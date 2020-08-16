/*
 * Memory merging support.
 *
 * This code enables dynamic sharing of identical pages found in different
 * memory areas, even if they are not shared by fork()
 *
 * Copyright (C) 2008-2009 Red Hat, Inc.
 * Authors:
 *	Izik Eidus
 *	Andrea Arcangeli
 *	Chris Wright
 *	Hugh Dickins
 *
 * This work is licensed under the terms of the GNU GPL, version 2.
 */

#include <linux/errno.h>
#include <linux/mm.h>
#include <linux/fs.h>
#include <linux/mman.h>
#include <linux/sched.h>
#include <linux/rwsem.h>
#include <linux/pagemap.h>
#include <linux/rmap.h>
#include <linux/spinlock.h>
#include <linux/jhash.h>
#include <linux/delay.h>
#include <linux/kthread.h>
#include <linux/wait.h>
#include <linux/slab.h>
#include <linux/rbtree.h>
#include <linux/memory.h>
#include <linux/mmu_notifier.h>
#include <linux/swap.h>
#include <linux/ksm.h>
#include <linux/hashtable.h>
#include <linux/freezer.h>
#include <linux/oom.h>
#include <linux/numa.h>

#include <linux/kernel.h> // printk

#include <asm/tlbflush.h>
#include "internal.h"

#include <asm/barrier.h>

#define SYST_NOINLINE
// #define SCAN_STEP_CNT

// #define VERBOS_GET_PKSM_PAGE
// #define VERBOS_TRY_TO_MERGE_ONE_PAGE
// #define MANUAL_PAGE_ADD
// #define VERBOS_PKSM_EXIT
// #define VERBOS_PKSM_NEW_ANON_PAGE
#define USE_ADVANCED_MEMCMP
// #define // perf_break_point_ON

// #ifdef // perf_break_point_ON



// #else

// #define // perf_break_point(g, p)

// #endif

// #define crc32_sse42

#define PARTIAL_HASH_LEN 256
#define TOTAL_HASH_LEN 4096

#ifdef USE_ADVANCED_MEMCMP

	#ifdef CONFIG_X86
		#undef memcmp
		#ifdef CONFIG_X86_32
			#define memcmp memcmpx86_32
			/*
			* Compare 4-byte-aligned address s1 and s2, with length n
			*/
			int memcmpx86_32(void *s1, void *s2, size_t n)
			{
				size_t num = n / 4;
				register int res;

				__asm__ __volatile__
				(
				"testl %3,%3\n\t"
				"repe; cmpsd\n\t"
				"je        1f\n\t"
				"sbbl      %0,%0\n\t"
				"orl       $1,%0\n"
				"1:"
				: "=&a" (res), "+&S" (s1), "+&D" (s2), "+&c" (num)
				: "0" (0)
				: "cc");

				return res;
			}

			static int is_full_zero(const void *s1, size_t len)
			{
				unsigned char same;

				len /= 4;

				__asm__ __volatile__
				("repe; scasl;"
				"sete %0"
				: "=qm" (same), "+D" (s1), "+c" (len)
				: "a" (0)
				: "cc");

				return same;
			}
		#elif defined(CONFIG_X86_64)
			#define memcmp memcmpx86_64
			/*
			* Compare 8-byte-aligned address s1 and s2, with length n
			*/
			int memcmpx86_64(void *s1, void *s2, size_t n)
			{
				size_t num = n / 8;
				register int res;

				__asm__ __volatile__
				(
				"testq %q3,%q3\n\t"
				"repe; cmpsq\n\t"
				"je        1f\n\t"
				"sbbq      %q0,%q0\n\t"
				"orq       $1,%q0\n"
				"1:"
				: "=&a" (res), "+&S" (s1), "+&D" (s2), "+&c" (num)
				: "0" (0)
				: "cc");

				return res;
			}

			static int is_full_zero(const void *s1, size_t len)
			{
				unsigned char same;

				len /= 8;

				__asm__ __volatile__
				("repe; scasq;"
				"sete %0"
				: "=qm" (same), "+D" (s1), "+c" (len)
				: "a" (0)
				: "cc");

				return same;
			}
		#endif
	#endif
#else
	static int is_full_zero(const void *s1, size_t len)
	{
		const unsigned long *src = s1;
		int i;

		len /= sizeof(*src);

		for (i = 0; i < len; i++) {
			if (src[i])
				return 0;
		}

		return 1;
	}
#endif

#ifdef CONFIG_NUMA
#define NUMA(x)		(x)
#define DO_NUMA(x)	do { (x); } while (0)
#else
#define NUMA(x)		(0)
#define DO_NUMA(x)	do { } while (0)
#endif

/*
 * A few notes about the KSM scanning process,
 * to make it easier to understand the data structures below:
 *
 * In order to reduce excessive scanning, KSM sorts the memory pages by their
 * contents into a data structure that holds pointers to the pages' locations.
 *
 * Since the contents of the pages may change at any moment, KSM cannot just
 * insert the pages into a normal sorted tree and expect it to find anything.
 * Therefore KSM uses two data structures - the stable and the unstable tree.
 *
 * The stable tree holds pointers to all the merged pages (ksm pages), sorted
 * by their contents.  Because each such page is write-protected, searching on
 * this tree is fully assured to be working (except when pages are unmapped),
 * and therefore this tree is called the stable tree.
 *
 * In addition to the stable tree, KSM uses a second data structure called the
 * unstable tree: this tree holds pointers to pages which have been found to
 * be "unchanged for a period of time".  The unstable tree sorts these pages
 * by their contents, but since they are not write-protected, KSM cannot rely
 * upon the unstable tree to work correctly - the unstable tree is liable to
 * be corrupted as its contents are modified, and so it is called unstable.
 *
 * KSM solves this problem by several techniques:
 *
 * 1) The unstable tree is flushed every time KSM completes scanning all
 *    memory areas, and then the tree is rebuilt again from the beginning.
 * 2) KSM will only insert into the unstable tree, pages whose hash value
 *    has not changed since the previous scan of all memory areas.
 * 3) The unstable tree is a RedBlack Tree - so its balancing is based on the
 *    colors of the nodes and not on their contents, assuring that even when
 *    the tree gets "corrupted" it won't get out of balance, so scanning time
 *    remains the same (also, searching and inserting nodes in an rbtree uses
 *    the same algorithm, so we have no overhead when we flush and rebuild).
 * 4) KSM never flushes the stable tree, which means that even if it were to
 *    take 10 attempts to find a page in the unstable tree, once it is found,
 *    it is secured in the stable tree.  (When we scan a new page, we first
 *    compare it against the stable tree, and then against the unstable tree.)
 *
 * If the merge_across_nodes tunable is unset, then KSM maintains multiple
 * stable trees and multiple unstable trees: one of each for each NUMA node.
 */

/**
 * 再利用rmap机制的时候只传递一个指针参数
 * 但是我们需要两个：kpage + stable_node
 * 所以用这个结构进行封装
 */
struct rmap_process_wrapper{
	struct pksm_hash_node *pksm_hash_node;
	struct page *kpage; 
};

/**
 * struct page_slot - ksm scanning basic unit change from mm(virtual memory) to page(physical memory)
 * @page_list: link into priority list 
 * @physical_page: point to struct page
 * @page_item: 在stable/unstable table中的结构
 * @invalid: 代表这个页面是否被exit掉，或者因为发生归并而变得无效
 * @link: 在page_to_slot_table中的结构
 * @mapcount: 记录当前page的映射数量，用于page_sharing统计量的准确性
 * @partial_hash: 记录partial_hash值（full_hash的值由hash table的索引完成） 
 */
struct page_slot {
	struct list_head page_list;	
	struct page *physical_page;	
	struct pksm_hash_node *page_item;
	bool invalid;
	struct hlist_node link;
	unsigned long mapcount;
	uint32_t partial_hash;
	unsigned long add_stamp;
};


struct pksm_scan{
	struct page_slot *page_slot;
	unsigned long seqnr;
};



struct pksm_rmap_item{
	struct hlist_node hlist;
	struct anon_vma *anon_vma;
	struct mm_struct *mm;
	unsigned long address;
};

#define PAGE_SLOTS_HASH_BITS 18
static DEFINE_HASHTABLE(page_slots_hash, PAGE_SLOTS_HASH_BITS);

struct pksm_hash_node{
	unsigned long kpfn;
    struct hlist_node hlist;
	struct page_slot *page_slot;
	struct hlist_head rmap_list;
};

#define PAGE_HASH_BIT 18 // 256K
#define PAGE_HASH_MASK 262143
static DEFINE_HASHTABLE(stable_hash_table, PAGE_HASH_BIT);
static DEFINE_HASHTABLE(unstable_hash_table, PAGE_HASH_BIT);

static struct page_slot pksm_page_head = {
	.page_list = LIST_HEAD_INIT(pksm_page_head.page_list),
};

static struct pksm_scan pksm_scan = {
	.page_slot = &pksm_page_head,
	.seqnr = 0,
};

static struct kmem_cache *pksm_hash_node_cache;
static struct kmem_cache *page_slot_cache;
static struct kmem_cache *pksm_rmap_item_cache;


/* The number of nodes in the stable tree */
static unsigned long pksm_pages_shared;

static unsigned long pksm_pages_sharing;

static unsigned long pksm_pages_merged;

/* The number of page slots additionally sharing those nodes */

static unsigned long pksm_pages_inlist;

static unsigned long pksm_node_items;
static unsigned long pksm_rmap_items;

// static unsigned int ksm_thread_pages_to_scan = 200;

// static unsigned int ksm_thread_sleep_millisecs = 20;

/* PKSM进程进入睡眠前需要连续扫描到的不可归并页面的数量 */
static unsigned int pksm_cont_unmerged_pages_threshold = 200;
static unsigned int pksm_scaned_pages_threshold = 10000000;

/* PKSM进程睡眠时间基准 */
static unsigned int pksm_thread_sleep_millisecs_base = 50;

/* PKSM进程真实睡眠时间基准 */
static unsigned int pksm_thread_sleep_millisecs_real;
static unsigned int pksm_thread_sleep_millisecs_low = 20;
static unsigned int pksm_thread_sleep_millisecs_high = 1000;

/* PKSM此趟归并数量 */
static unsigned int pksm_cur_merged_pages = 1;
static unsigned int pksm_last_merged_pages = 1;

/* PKSM此趟未归并数量 */
static unsigned int pksm_cur_unmerged_pages = 1;
static unsigned int pksm_last_unmerged_pages = 1;

/* 当前连续不可归并连续页面数量 */
static unsigned int pksm_cur_cont_unmerged_pages = 0;

/* 扫描的步长 */
static unsigned int pksm_scan_steps[5] = {3, 7, 17, 29, 41};
static unsigned int pksm_cur_scan_step = 17;

static unsigned int pksm_scan_step_cnts[5] = {0, 0, 0, 0, 0};
static unsigned int pksm_scan_step_pervage_cnts[6] = {0, 0, 0, 0, 0, 0};

/* 当前扫描的状态 */
static unsigned int pksm_scan_status = 0;

/* 发生零归并的次数 */
static unsigned long pksm_zero_merged = 0;

static int unstable_cnt_bucket = 0;
static int stable_cnt_bucket = 0;

/* 零页面的哈希 */
static u32 zero_hash __read_mostly;

/* 上一个获取的页面的时间戳 */
// static unsigned int pksm_pre_stamp = 0;

/* stamp差值与step的对应关系 */
static unsigned int pksm_step_level[11] = {
	4, 4,		/* 0, 1 */
	3, 3,		/* 2, 3 */
	2, 2, 2,	/* 4, 5, 6 */
	1, 1, 1, 1	/* 7, 8, 9, 10 */
};
/* 在本次扫描过程中新加入的页面 */
static unsigned long pksm_new_pages_inlist = 0;



#ifdef CONFIG_NUMA
/* Zeroed when merging across nodes is not allowed */
static unsigned int ksm_merge_across_nodes = 1;
static int ksm_nr_node_ids = 1;
#else
#define ksm_merge_across_nodes	1U
#define ksm_nr_node_ids		1
#endif

#define PKSM_RUN_STOP	0
#define PKSM_RUN_MERGE	1
#define PKSM_RUN_UNMERGE	2
#define PKSM_RUN_OFFLINE	4
static unsigned long pksm_run = PKSM_RUN_STOP;
static void wait_while_offlining(void);

static DECLARE_WAIT_QUEUE_HEAD(pksm_thread_wait);
static DEFINE_MUTEX(pksm_thread_mutex);
static DEFINE_SPINLOCK(pksm_pagelist_lock);




// ============================ crc32_hw begin ======================================
#ifdef crc32_sse42
#include <smmintrin.h>

#define ALIGN_SIZE      0x08UL
#define ALIGN_MASK      (ALIGN_SIZE - 1)
#define CALC_CRC(op, crc, type, buf, len)                               \
  do {                                                                  \
    for (; (len) >= sizeof (type); (len) -= sizeof(type), buf += sizeof (type)) { \
      (crc) = op((crc), *(type *) (buf));                               \
    }                                                                   \
  } while(0)

uint32_t crc32c_hw(const void *input, int len, uint32_t crc)
{
    const char* buf = (const char*)input;

    // XOR the initial CRC with INT_MAX
    crc ^= 0xFFFFFFFF;

    // Align the input to the word boundary
    for (; (len > 0) && ((size_t)buf & ALIGN_MASK); len--, buf++) {
        crc = _mm_crc32_u8(crc, *buf);
    }

    // Blast off the CRC32 calculation
    CALC_CRC(_mm_crc32_u64, crc, uint64_t, buf, len);
    CALC_CRC(_mm_crc32_u32, crc, uint32_t, buf, len);
    CALC_CRC(_mm_crc32_u16, crc, uint16_t, buf, len);
    CALC_CRC(_mm_crc32_u8, crc, uint8_t, buf, len);

    // Post-process the crc
    return (crc ^ 0xFFFFFFFF);
}
#endif
// ============================ crc32_hw end ======================================


// ============================ super fast hash begin ======================================

// #undef get16bits
// #if (defined(__GNUC__) && defined(__i386__)) || defined(__WATCOMC__) \
//   || defined(_MSC_VER) || defined (__BORLANDC__) || defined (__TURBOC__)
// #define get16bits(d) (*((const uint16_t *) (d)))
// #endif

// #if !defined (get16bits)
// #define get16bits(d) ((((uint32_t)(((const uint8_t *)(d))[1])) << 8)\
//                        +(uint32_t)(((const uint8_t *)(d))[0]) )
// #endif
#define get16bits(d) (*((const uint16_t *) (d)))
#define get32bits(d) (*((const uint32_t *) (d)))


// static uint32_t super_fast_hash_comp(const char * data, int len, uint32_t *partial_hash)
// {
//     uint32_t hash = len, tmp;
//     int rem;
// 	int partial_len = PARTIAL_HASH_LEN >> 2;

//     if (len <= 0 || data == NULL) return 0;

// 	__builtin_prefetch(data, 0, 3);
// 	__builtin_prefetch(data+4, 0, 3);


//     // rem = len & 3;
//     len >>= 2;
// 	len -= partial_len;

//     /* Main loop */
//     for (;partial_len > 0; partial_len--) {
// 		__builtin_prefetch(data+8, 0, 3);
//         hash  += get16bits (data);
//         tmp    = (get16bits (data+2) << 11) ^ hash;
//         hash   = (hash << 16) ^ tmp;
//         data  += 2*sizeof (uint16_t);
//         hash  += hash >> 11;
//     }

// 	*partial_hash = hash;

// 	for (;len > 0; len--) {
// 		__builtin_prefetch(data+8, 0, 3);
//         hash  += get16bits (data);
//         tmp    = (get16bits (data+2) << 11) ^ hash;
//         hash   = (hash << 16) ^ tmp;
//         data  += 2*sizeof (uint16_t);
//         hash  += hash >> 11;
// 	}

//     /* Force "avalanching" of final 127 bits */
//     hash ^= hash << 3;
//     hash += hash >> 5;
//     hash ^= hash << 4;
//     hash += hash >> 17;
//     hash ^= hash << 25;
//     hash += hash >> 6;

//     return hash;
// }

static uint32_t super_fast_hash_simp(const char * data, int len, uint32_t seed)
{
    uint32_t hash = seed, tmp;

    if (len <= 0 || data == NULL) return 0;

	// __builtin_prefetch(data, 0, 3);

    // rem = len & 3;
    len >>= 2;


	for (;len > 0; len--) {
		// __builtin_prefetch(data+4, 0, 3);
        hash  += get16bits (data);
        tmp    = (get16bits (data+2) << 11) ^ hash;
        hash   = (hash << 16) ^ tmp;
        data  += 2*sizeof (uint16_t);
        hash  += hash >> 11;
	}

    /* Force "avalanching" of final 127 bits */
    hash ^= hash << 3;
    hash += hash >> 5;
    hash ^= hash << 4;
    hash += hash >> 17;
    hash ^= hash << 25;
    hash += hash >> 6;

    return hash;
}

static uint32_t super_fast_hash_simp_unloop2(const char * data, int len, uint32_t seed)
{
    uint32_t hash = seed, hash2 = 0, tmp, tmp2;

    if (len <= 0 || data == NULL) return 0;

	// __builtin_prefetch(data, 0, 3);

    // rem = len & 3;
    len >>= 3;


	for (;len > 0; len--) {
		// __builtin_prefetch(data+4, 0, 3);
        hash  += get16bits (data);
		hash2 += get16bits (data+2);

        tmp    = (get16bits (data+4) << 11) ^ hash;
        tmp2    = (get16bits (data+6) << 11) ^ hash2;

        hash   = (hash << 16) ^ tmp;
        hash2   = (hash2 << 16) ^ tmp2;

        data  += 4*sizeof (uint16_t);

        hash  += hash >> 11;
        hash2  += hash2 >> 11;
	}

	hash ^= hash2;

    /* Force "avalanching" of final 127 bits */
    hash ^= hash << 3;
    hash += hash >> 5;
    hash ^= hash << 4;
    hash += hash >> 17;
    hash ^= hash << 25;
    hash += hash >> 6;

    return hash;
}

static uint64_t super_fast_hash_64(const char * data, int len, uint64_t seed)
{
    uint64_t hash = seed, tmp;

    if (len <= 0 || data == NULL) return 0;

	// printk("PKSM : super_fast_hash_64 : %p\n", data);

	// __builtin_prefetch(data, 0, 3);

    // rem = len & 3;
    len >>= 3;


	for (;len > 0; len--) {
		// __builtin_prefetch(data+4, 0, 3);
        hash  += get32bits (data);
        tmp    = (((const uint64_t)get32bits (data+4)) << 22) ^ hash;
        hash   = (hash << 32) ^ tmp;
        data  += 2*sizeof (uint32_t);
        hash  += hash >> 22;
	}

    /* Force "avalanching" of final 127 bits */
    hash ^= hash << 6;
    hash += hash >> 10;
    hash ^= hash << 8;
    hash += hash >> 34;
    hash ^= hash << 50;
    hash += hash >> 12;

	hash ^= hash >> 32;

    return hash;
}

static uint64_t super_fast_hash_64_unloop(const char * data, int len, uint64_t seed)
{
    uint64_t hash = seed, hash2 = 0, tmp, tmp2;

    if (len <= 0 || data == NULL) return 0;

	// printk("PKSM : super_fast_hash_64 : %p\n", data);

	// __builtin_prefetch(data, 0, 3);

    // rem = len & 3;
    len >>= 4;


	for (;len > 0; len--) {
		// __builtin_prefetch(data+4, 0, 3);
        hash  += get32bits (data);
        hash2  += get32bits (data+4);

        tmp    = (((const uint64_t)get32bits (data+8)) << 22) ^ hash;
        tmp2    = (((const uint64_t)get32bits (data+12)) << 22) ^ hash2;

        hash   = (hash << 32) ^ tmp;
        hash2   = (hash2 << 32) ^ tmp2;

        data  += 4*sizeof (uint32_t);

        hash  += hash >> 22;
        hash2  += hash2 >> 22;
	}

	hash ^= hash2;

    /* Force "avalanching" of final 127 bits */
    hash ^= hash << 6;
    hash += hash >> 10;
    hash ^= hash << 8;
    hash += hash >> 34;
    hash ^= hash << 50;
    hash += hash >> 12;

	hash ^= hash >> 32;

    return hash;
}

// ============================ super fast hash end ======================================


#ifdef SYST_NOINLINE
static noinline u32 calc_hash(struct page *page, uint32_t *partial_hash)
#else
static u32 calc_hash(struct page *page, uint32_t *partial_hash)
#endif
{
	char *addr;
	u32 checksum;

	addr = kmap_atomic(page);
	// checksum = super_fast_hash(addr, PAGE_SIZE);

	// checksum = super_fast_hash(addr, PAGE_SIZE, partial_hash);

	// *partial_hash = crc32c_hw(addr, PARTIAL_HASH_LEN, 0);
	// checksum = crc32c_hw(addr+PARTIAL_HASH_LEN, PAGE_SIZE-PARTIAL_HASH_LEN, *partial_hash);
	
	// *partial_hash = super_fast_hash_simp(addr, PARTIAL_HASH_LEN, TOTAL_HASH_LEN);
	// checksum = super_fast_hash_simp(addr+PARTIAL_HASH_LEN, TOTAL_HASH_LEN-PARTIAL_HASH_LEN, *partial_hash);

	// *partial_hash = super_fast_hash_64(addr, PARTIAL_HASH_LEN, TOTAL_HASH_LEN);
	// checksum = super_fast_hash_64(addr+PARTIAL_HASH_LEN, TOTAL_HASH_LEN-PARTIAL_HASH_LEN, *partial_hash);

	*partial_hash = super_fast_hash_64_unloop(addr, PARTIAL_HASH_LEN, TOTAL_HASH_LEN);
	checksum = super_fast_hash_64_unloop(addr+PARTIAL_HASH_LEN, TOTAL_HASH_LEN-PARTIAL_HASH_LEN, *partial_hash);

	kunmap_atomic(addr);
	return checksum;
}

#ifdef SYST_NOINLINE
static noinline u32 calc_partial_hash(struct page *page)
#else
static u32 calc_partial_hash(struct page *page)
#endif
{
	char *addr;
	u32 checksum;

	addr = kmap_atomic(page);

	checksum = super_fast_hash_64_unloop(addr, PARTIAL_HASH_LEN, TOTAL_HASH_LEN);

	kunmap_atomic(addr);

	return checksum;
}

// static noinline void perf_break_point(int group_number, int point_number){
// 	__asm__ __volatile__("": : :"memory");
// 	mb();
// }


#define PKSM_KMEM_CACHE(__struct, __flags) kmem_cache_create("pksm_"#__struct,\
		sizeof(struct __struct), __alignof__(struct __struct),\
		(__flags), NULL)



static int __init pksm_slab_init(void)
{
	pksm_hash_node_cache = PKSM_KMEM_CACHE(pksm_hash_node, 0);
	if (!pksm_hash_node_cache)
		goto out;

	page_slot_cache = PKSM_KMEM_CACHE(page_slot, 0);
	if (!page_slot_cache)
		goto out_free1;

	pksm_rmap_item_cache = PKSM_KMEM_CACHE(pksm_rmap_item, 0);
	if (!pksm_rmap_item_cache)
		goto out_free2;

	return 0;

out_free2:
	kmem_cache_destroy(page_slot_cache);
out_free1:
	kmem_cache_destroy(pksm_hash_node_cache);
out:
	return -ENOMEM;
}



static void __init pksm_slab_free(void)
{
	kmem_cache_destroy(pksm_hash_node_cache);
	kmem_cache_destroy(page_slot_cache);
	kmem_cache_destroy(pksm_rmap_item_cache);
	page_slot_cache = NULL; // 为什么就他这么突出？
}


// * pksm begin

static inline struct pksm_rmap_item *alloc_pksm_rmap_item(void)
{
	++pksm_rmap_items;
	return kmem_cache_alloc(pksm_rmap_item_cache, GFP_KERNEL);
}

static inline void free_pksm_rmap_item(struct pksm_rmap_item *pksm_rmap_item)
{
	kmem_cache_free(pksm_rmap_item_cache, pksm_rmap_item);
	--pksm_rmap_items;
}

static inline struct pksm_hash_node *alloc_hash_node(void)
{
	++pksm_node_items;
	return kmem_cache_alloc(pksm_hash_node_cache, GFP_KERNEL);
}

static inline void free_hash_node(struct pksm_hash_node *pksm_hash_node)
{
	kmem_cache_free(pksm_hash_node_cache, pksm_hash_node);
	--pksm_node_items;
}

static inline struct page_slot *alloc_page_slot(void)
{
	if (!page_slot_cache)	/* initialization failed */
		return NULL;
	++pksm_pages_inlist;
	return kmem_cache_zalloc(page_slot_cache, GFP_ATOMIC);	//KERNEL会造成阻塞，在缺页中断中产生带锁调度导致死锁
}

static inline void free_page_slot(struct page_slot *page_slot)
{
	kmem_cache_free(page_slot_cache, page_slot);
	--pksm_pages_inlist;
}

static struct page_slot *get_page_slot(struct page *page)
{
	struct page_slot *slot;
	struct hlist_head *head;

	hash_for_each_possible(page_slots_hash, slot, link, (unsigned long)page)
		if (slot->physical_page == page)
			return slot;

	return NULL;
}

static void insert_into_page_slots_hash(struct page *page,
				    struct page_slot *page_slot)
{
	page_slot->physical_page = page;
	hash_add(page_slots_hash, &page_slot->link, (unsigned long)page);
}

static void remove_from_page_slots_hash(struct page_slot *page_slot)
{
	hash_del(&page_slot->link);
}

static inline bool page_slot_not_in_hash_table(struct page_slot *page_slot)
{
	return (page_slot->page_item == NULL || page_slot->page_item == page_slot);
}

static inline bool page_slot_in_hash_table(struct page_slot *page_slot)
{
	return !page_slot_not_in_hash_table(page_slot);
}

// * pksm end


static inline bool pksm_test_exit(struct page_slot *page_slot)
{
	// 这里暂时使用page->_mapcount
	return (page_slot->invalid) || (page_count(page_slot->physical_page) == 0) || (page_mapcount(page_slot->physical_page) == 0);
}

static inline bool ksm_test_exit(struct mm_struct *mm)
{
	return atomic_read(&mm->mm_users) == 0;
}

static int count_rmap_item_num(struct pksm_hash_node* pksm_hash_node)
{
	int cnt = 0;
	struct pksm_rmap_item* pksm_rmap_item;
	struct hlist_node *nxt;

	if(!hlist_empty(&(pksm_hash_node->rmap_list))){
		hlist_for_each_entry_safe(pksm_rmap_item, nxt, &(pksm_hash_node->rmap_list), hlist){
			++cnt;
		}
	}

	return cnt;
}

static int break_ksm(struct vm_area_struct *vma, unsigned long addr)
{
	struct page *page;
	int ret = 0;

	do {
		// cond_resched();
		// TODO: 因为我们操作的本来就是physical_page，这里可以直接把page传进来
		page = follow_page(vma, addr,
				FOLL_GET | FOLL_MIGRATION | FOLL_REMOTE);
		if (IS_ERR_OR_NULL(page))
			break;
		if (PagePksm_inline(page))
			ret = handle_mm_fault(vma, addr,
					FAULT_FLAG_WRITE | FAULT_FLAG_REMOTE);
		else
			ret = VM_FAULT_WRITE;
		put_page(page);
	} while (!(ret & (VM_FAULT_WRITE | VM_FAULT_SIGBUS | VM_FAULT_SIGSEGV | VM_FAULT_OOM)));
	/*
	 * We must loop because handle_mm_fault() may back out if there's
	 * any difficulty e.g. if pte accessed bit gets updated concurrently.
	 *
	 * VM_FAULT_WRITE is what we have been hoping for: it indicates that
	 * COW has been broken, even if the vma does not permit VM_WRITE;
	 * but note that a concurrent fault might break PageKsm for us.
	 *
	 * VM_FAULT_SIGBUS could occur if we race with truncation of the
	 * backing file, which also invalidates anonymous pages: that's
	 * okay, that truncation will have unmapped the PageKsm for us.
	 *
	 * VM_FAULT_OOM: at the time of writing (late July 2009), setting
	 * aside mem_cgroup limits, VM_FAULT_OOM would only be set if the
	 * current task has TIF_MEMDIE set, and will be OOM killed on return
	 * to user; and ksmd, having no mm, would never be chosen for that.
	 *
	 * But if the mm is in a limited mem_cgroup, then the fault may fail
	 * with VM_FAULT_OOM even if the current task is not TIF_MEMDIE; and
	 * even ksmd can fail in this way - though it's usually breaking ksm
	 * just to undo a merge it made a moment before, so unlikely to oom.
	 *
	 * That's a pity: we might therefore have more kernel pages allocated
	 * than we're counting as nodes in the stable tree; but ksm_do_scan
	 * will retry to break_cow on each pass, so should recover the page
	 * in due course.  The important thing is to not let VM_MERGEABLE
	 * be cleared while any such pages might remain in the area.
	 */
	return (ret & VM_FAULT_OOM) ? -ENOMEM : 0;
}

static struct vm_area_struct *find_mergeable_vma(struct mm_struct *mm,
		unsigned long addr)
{
	struct vm_area_struct *vma;
	if (ksm_test_exit(mm))
		return NULL;
	vma = find_vma(mm, addr);
	if (!vma || vma->vm_start > addr)
		return NULL;
	// if (!(vma->vm_flags & VM_MERGEABLE) || !vma->anon_vma)
	if (!vma->anon_vma)
		return NULL;
	return vma;
}

static void break_cow(struct page_slot* page_slot, struct pksm_hash_node* pksm_hash_node)
{

	struct mm_struct *mm;
	unsigned long addr;
	struct vm_area_struct *vma;
	struct pksm_rmap_item* pksm_rmap_item;
	struct hlist_node *nxt;
	int err = 0;

	// printk("PKSM : break_cow called\n");

	if(count_rmap_item_num(pksm_hash_node) != 1){
		printk(KERN_ALERT "PKSM : \tbug occur not 1");
		printk(KERN_ALERT "PKSM : \tslot: %p, rmapcnt: %d, page: %p, refcount: %d, mapcount: %d, isPKSM: %d\n", page_slot, count_rmap_item_num(pksm_hash_node), page_slot->physical_page, page_ref_count(page_slot->physical_page), page_mapcount(page_slot->physical_page), PagePksm(page_slot->physical_page));
	}else{
		//TODO: 反正就一个元素，可以从循环里拆出来
		hlist_for_each_entry_safe(pksm_rmap_item, nxt, &(pksm_hash_node->rmap_list), hlist){
			mm = pksm_rmap_item->mm;
			addr = pksm_rmap_item->address;

			put_anon_vma(pksm_rmap_item->anon_vma);

			down_read(&mm->mmap_sem);
			vma = find_mergeable_vma(mm, addr);
			if (vma){
				err = break_ksm(vma, addr);
				// printk("PKSM : break_cow -> break_ksm: %d\n", err);
			}else{
				printk(KERN_ALERT "PKSM : \tbug occur no vma");
			}

			up_read(&mm->mmap_sem);
		}
	}

	// if(page_slot_not_in_hash_table(page_slot)){
	// 	printk("PKSM : bug occur, count_rmap_item_num");
		// printk("PKSM : \tslot: %p, page: %p, refcount: %d, mapcount: %d\n", page_slot, page_slot->physical_page, page_ref_count(page_slot->physical_page), page_mapcount(page_slot->physical_page));

	// }else{
	// }	
}


static struct page *page_trans_compound_anon(struct page *page)
{
	printk(KERN_ALERT "PKSM : empty_function : page_trans_compound_anon evoked\n");
	return NULL;
	
}


// 把inline去掉了
static void free_all_rmap_item_of_node(struct pksm_hash_node *pksm_hash_node){
	struct pksm_rmap_item* pksm_rmap_item;
	struct hlist_node *nxt;
	if(!hlist_empty(&(pksm_hash_node->rmap_list))){
		hlist_for_each_entry_safe(pksm_rmap_item, nxt, &(pksm_hash_node->rmap_list), hlist){
			put_anon_vma(pksm_rmap_item->anon_vma);
			free_pksm_rmap_item(pksm_rmap_item);
			// cond_resched();
			// --pksm_pages_sharing;
		}
		--pksm_pages_shared;
		// 这里没有计数泄漏
		// 因为slot->mapcount直接和sharing相关，如果使用page的真实count，其中可能会有没有遗漏的释放，导致减的太少
		pksm_pages_sharing -= pksm_hash_node->page_slot->mapcount;
	}
}



static void remove_node_from_hashlist(struct page_slot *page_slot)
{
	if(page_slot_in_hash_table(page_slot)){	// 如果他在哈希表里有残留（不管是stable还是unstable）
		// printk("PKSM : remove_node_from_hashlist : slot: %p, page: %p, item: %p\n", page_slot, page_slot->physical_page, page_slot->page_item);
		hlist_del(&(page_slot->page_item->hlist));	// 都将他删除

		// 递归释放所有的rmap_item对象
		free_all_rmap_item_of_node(page_slot->page_item);

		free_hash_node(page_slot->page_item);
		page_slot->page_item = NULL;
	}

}

static void remove_node_from_hashlist_not_null(struct page_slot *page_slot)
{
	if(page_slot_in_hash_table(page_slot)){	// 如果他在哈希表里有残留（不管是stable还是unstable）
		// printk("PKSM : remove_node_from_hashlist : slot: %p, page: %p, item: %p\n", page_slot, page_slot->physical_page, page_slot->page_item);
		hlist_del(&(page_slot->page_item->hlist));	// 都将他删除

		// 递归释放所有的rmap_item对象
		free_all_rmap_item_of_node(page_slot->page_item);

		free_hash_node(page_slot->page_item);
		page_slot->page_item = (struct pksm_hash_node*)page_slot;
	}

}

/*
 * get_ksm_page: checks if the page indicated by the stable node
 * is still its ksm page, despite having held no reference to it.
 * In which case we can trust the content of the page, and it
 * returns the gotten page; but if the page has now been zapped,
 * remove the stale node from the stable tree and return NULL.
 * But beware, the stable node's page might be being migrated.
 *
 * You would expect the stable_node to hold a reference to the ksm page.
 * But if it increments the page's count, swapping out has to wait for
 * ksmd to come around again before it can free the page, which may take
 * seconds or even minutes: much too unresponsive.  So instead we use a
 * "keyhole reference": access to the ksm page from the stable node peeps
 * out through its keyhole to see if that page still holds the right key,
 * pointing back to this stable node.  This relies on freeing a PageAnon
 * page to reset its page->mapping to NULL, and relies on no other use of
 * a page to put something that might look like our key in page->mapping.
 * is on its way to being freed; but it is an anomaly to bear in mind.
 */
static struct page *get_pksm_page(struct pksm_hash_node *stable_node, bool lock_it)
{
	struct page *page;
	void *expected_mapping;
	unsigned long kpfn;


	expected_mapping = (void *)stable_node +
				(PAGE_MAPPING_ANON | PAGE_MAPPING_KSM);
again:
	kpfn = READ_ONCE(stable_node->kpfn);
	page = pfn_to_page(kpfn);

#ifdef VERBOS_GET_PKSM_PAGE
	// printk("PKSM : get_pksm_page : kpfn: %lu\n", kpfn);
	// printk("PKSM : get_pksm_page : node: %p, page: %p\n", stable_node, page);
	// if(stable_node != NULL){
		// printk("PKSM : get_pksm_page : slot: %p\n", stable_node->page_slot);
		// if(stable_node->page_slot != NULL){
			// printk("PKSM : get_pksm_page : page: %p, node: %p\n", stable_node->page_slot->physical_page, stable_node->page_slot->page_item);
		// }else{
			// printk("PKSM : get_pksm_page : page_slot=null\n");
			
		// }
	// }else{
		// printk("PKSM : get_pksm_page : stable_node=null\n");
		
	// }
#endif

#ifdef VERBOS_GET_PKSM_PAGE
	// printk("PKSM : get_pksm_page : 1\n");
#endif
	/*
	 * page is computed from kpfn, so on most architectures reading
	 * page->mapping is naturally ordered after reading node->kpfn,
	 * but on Alpha we need to be more careful.
	 */
	smp_read_barrier_depends();
#ifdef VERBOS_GET_PKSM_PAGE
	// printk("PKSM : get_pksm_page : 1.1 : page_mapping: %p, expect_mappint: %p\n", page->mapping, expected_mapping);
#endif
	if (READ_ONCE(page->mapping) != expected_mapping)
		goto stale;

#ifdef VERBOS_GET_PKSM_PAGE
	// printk("PKSM : get_pksm_page : 2\n");
#endif

	/*
	 * We cannot do anything with the page while its refcount is 0.
	 * Usually 0 means free, or tail of a higher-order page: in which
	 * case this node is no longer referenced, and should be freed;
	 * however, it might mean that the page is under page_freeze_refs().
	 * The __remove_mapping() case is easy, again the node is now stale;
	 * but if page is swapcache in migrate_page_move_mapping(), it might
	 * still be our page, in which case it's essential to keep the node.
	 */
	while (!get_page_unless_zero(page)) {
		/*
		 * Another check for page->mapping != expected_mapping would
		 * work here too.  We have chosen the !PageSwapCache test to
		 * optimize the common case, when the page is or is about to
		 * be freed: PageSwapCache is cleared (under spin_lock_irq)
		 * in the freeze_refs section of __remove_mapping(); but Anon
		 * page->mapping reset to NULL later, in free_pages_prepare().
		 */
		if (!PageSwapCache(page))
			goto stale;
		cpu_relax();
	}
#ifdef VERBOS_GET_PKSM_PAGE
	// printk("PKSM : get_pksm_page : 3\n");
#endif


	if (READ_ONCE(page->mapping) != expected_mapping) {
		put_page(page);
		goto stale;
	}
#ifdef VERBOS_GET_PKSM_PAGE
	// printk("PKSM : get_pksm_page : 4\n");
#endif


	if (lock_it) {
		lock_page(page);
		if (READ_ONCE(page->mapping) != expected_mapping) {
			unlock_page(page);
			put_page(page);
			goto stale;
		}
	}
#ifdef VERBOS_GET_PKSM_PAGE
	// printk("PKSM : get_pksm_page : 5\n");
#endif

	return page;

stale:
	/*
	 * We come here from above when page->mapping or !PageSwapCache
	 * suggests that the node is stale; but it might be under migration.
	 * We need smp_rmb(), matching the smp_wmb() in ksm_migrate_page(),
	 * before checking whether node->kpfn has been changed.
	 */
#ifdef VERBOS_GET_PKSM_PAGE
	// printk("PKSM : get_pksm_page : page staled\n");
#endif
	smp_rmb();
	if (READ_ONCE(stable_node->kpfn) != kpfn)
		goto again;
	remove_node_from_hashlist(stable_node->page_slot);
	return NULL;
}


static int memcmp_pages(struct page *page1, struct page *page2)
{
	char *addr1, *addr2;
	int ret;

	addr1 = kmap_atomic(page1);
	addr2 = kmap_atomic(page2);
	ret = memcmp(addr1, addr2, PAGE_SIZE);
	kunmap_atomic(addr2);
	kunmap_atomic(addr1);
	return ret;
}

static inline int pages_identical(struct page *page1, struct page *page2)
{
	return !memcmp_pages(page1, page2);
}

static inline int is_page_full_zero(struct page *page)
{
	char *addr;
	int ret;

	addr = kmap_atomic(page);
	ret = is_full_zero(addr, PAGE_SIZE);
	kunmap_atomic(addr);

	return ret;
}

static int write_protect_page(struct vm_area_struct *vma, struct page *page,
			      pte_t *orig_pte)
{
	struct mm_struct *mm = vma->vm_mm;
	struct page_vma_mapped_walk pvmw = {
		.page = page,
		.vma = vma,
	};
	int swapped;
	int err = -EFAULT;
	unsigned long mmun_start;	/* For mmu_notifiers */
	unsigned long mmun_end;		/* For mmu_notifiers */

	pvmw.address = page_address_in_vma(page, vma);
	if (pvmw.address == -EFAULT)
		goto out;

	BUG_ON(PageTransCompound(page));

	mmun_start = pvmw.address;
	mmun_end   = pvmw.address + PAGE_SIZE;
	mmu_notifier_invalidate_range_start(mm, mmun_start, mmun_end);

	if (!page_vma_mapped_walk(&pvmw))
		goto out_mn;
	if (WARN_ONCE(!pvmw.pte, "Unexpected PMD mapping?"))
		goto out_unlock;

	if (pte_write(*pvmw.pte) || pte_dirty(*pvmw.pte) ||
	    (pte_protnone(*pvmw.pte) && pte_savedwrite(*pvmw.pte)) ||
						mm_tlb_flush_pending(mm)) {
		pte_t entry;

		swapped = PageSwapCache(page);
		flush_cache_page(vma, pvmw.address, page_to_pfn(page));
		/*
		 * Ok this is tricky, when get_user_pages_fast() run it doesn't
		 * take any lock, therefore the check that we are going to make
		 * with the pagecount against the mapcount is racey and
		 * O_DIRECT can happen right after the check.
		 * So we clear the pte and flush the tlb before the check
		 * this assure us that no O_DIRECT can happen after the check
		 * or in the middle of the check.
		 */
		entry = ptep_clear_flush_notify(vma, pvmw.address, pvmw.pte);
		/*
		 * Check that no O_DIRECT or similar I/O is in progress on the
		 * page
		 */
		if (page_mapcount(page) + 1 + swapped != page_count(page)) {
			set_pte_at(mm, pvmw.address, pvmw.pte, entry);
			goto out_unlock;
		}
		if (pte_dirty(entry))
			set_page_dirty(page);

		if (pte_protnone(entry))
			entry = pte_mkclean(pte_clear_savedwrite(entry));
		else
			entry = pte_mkclean(pte_wrprotect(entry));
		set_pte_at_notify(mm, pvmw.address, pvmw.pte, entry);
	}
	*orig_pte = *pvmw.pte;
	err = 0;

out_unlock:
	page_vma_mapped_walk_done(&pvmw);
out_mn:
	mmu_notifier_invalidate_range_end(mm, mmun_start, mmun_end);
out:
	return err;
}

// TODO: UKSM有一个自己的replace实现，可以试一下
// 这里暂时模仿KSM的实现方法
/**
 * replace_page - replace page in vma by new ksm page
 * @vma:      vma that holds the pte pointing to page
 * @page:     the page we are replacing by kpage
 * @kpage:    the ksm page we replace page by
 * @orig_pte: the original value of the pte
 *
 * Returns 0 on success, -EFAULT on failure.
 */
static int replace_page(struct vm_area_struct *vma, struct page *page,
			struct page *kpage, pte_t orig_pte)
{
	struct mm_struct *mm = vma->vm_mm;
	pmd_t *pmd;
	pte_t *ptep;
	pte_t newpte;
	spinlock_t *ptl;
	unsigned long addr;
	int err = -EFAULT;
	unsigned long mmun_start;	/* For mmu_notifiers */
	unsigned long mmun_end;		/* For mmu_notifiers */

	addr = page_address_in_vma(page, vma);
	if (addr == -EFAULT)
		goto out;

	pmd = mm_find_pmd(mm, addr);
	if (!pmd)
		goto out;

	mmun_start = addr;
	mmun_end   = addr + PAGE_SIZE;
	mmu_notifier_invalidate_range_start(mm, mmun_start, mmun_end);

	ptep = pte_offset_map_lock(mm, pmd, addr, &ptl);
	if (!pte_same(*ptep, orig_pte)) {
		pte_unmap_unlock(ptep, ptl);
		goto out_mn;
	}

	flush_cache_page(vma, addr, pte_pfn(*ptep));
	ptep_clear_flush_notify(vma, addr, ptep);
	newpte = mk_pte(kpage, vma->vm_page_prot);

	if ((page_to_pfn(kpage) == pksm_zero_pfn) || (page_to_pfn(kpage) == zero_pfn)) {
		newpte = pte_mkspecial(newpte);
		dec_mm_counter(mm, MM_ANONPAGES);
	} else {
		get_page(kpage);
		page_add_anon_rmap(kpage, vma, addr, false);
	}

	set_pte_at_notify(mm, addr, ptep, newpte);

	page_remove_rmap(page, false);
	if (!page_mapped(page))
		try_to_free_swap(page);
	put_page(page);

	pte_unmap_unlock(ptep, ptl);
	err = 0;
out_mn:
	mmu_notifier_invalidate_range_end(mm, mmun_start, mmun_end);
out:
	return err;
}


// TODO: 这个函数虽然没有用（因为我们不考虑大页），但是会被用到，所以不删
static int page_trans_compound_anon_split(struct page *page)
{
	int ret = 0;
	struct page *transhuge_head = page_trans_compound_anon(page);

	// printk("PKSM : page_trans_compound_anon_split evoked\n");

	if (transhuge_head) {
		/* Get the reference on the head to split it. */
		if (get_page_unless_zero(transhuge_head)) {
			/*
			 * Recheck we got the reference while the head
			 * was still anonymous.
			 */
			if (PageAnon(transhuge_head))
				ret = split_huge_page(transhuge_head);
			else
				/*
				 * Retry later if split_huge_page run
				 * from under us.
				 */
				ret = 1;
			put_page(transhuge_head);
		} else
			/* Retry later if split_huge_page run from under us. */
			ret = 1;
	}
	return ret;
}

static
bool try_to_merge_zero_page(struct page *page, struct vm_area_struct *vma,
		     unsigned long address, void *arg)
{
	struct page *zero_page = empty_pksm_zero_page;
	struct mm_struct *mm = vma->vm_mm;
	pte_t orig_pte = __pte(0);
	int err = -EFAULT;

	if (ksm_test_exit(mm))
		goto out;

	if (!trylock_page(page))
		goto out;

	if (!PageAnon(page))
		goto out_unlock;

	if (PageTransCompound(page)) {
		err = split_huge_page(page);
		if (err)
			goto out_unlock;
	}

	if (write_protect_page(vma, page, &orig_pte) == 0) {
		if (is_page_full_zero(page))
			err = replace_page(vma, page, zero_page, orig_pte);
	}

out_unlock:
	unlock_page(page);
out:
	if(err == 0){			// err==0代表操作成功
		++pksm_pages_sharing;
		return true;	// 反向映射模块定义的标志字段，代表此次操作成功，继续遍历
	}else{
		return false;	// 此次操作失败，反向映射遍历终止
							//? 只是一次失败就需要终止整个遍历过程吗？
	}
}

// static bool try_to_merge_zero_page(struct page *page, struct vm_area_struct *vma,
// 		     unsigned long address, void *arg)
// {

// 	struct page *zero_page = empty_pksm_zero_page;
// 	pte_t orig_pte = __pte(0);
// 	int err = -EFAULT;

// 	if (page == zero_page)			/* ksm page forked */
// 		return 0;

// 	if(ksm_test_exit(vma->vm_mm)){
// 		return true;
// 	}
	

// 	// 这里是ksm用于判断这个虚地址空间是否应该参与merge的标志
// 	// pksm里不用，直接全部merge
// 	// if (!(vma->vm_flags & VM_MERGEABLE))
// 	// 	goto out;

	
// 	if (PageTransCompound(page) && page_trans_compound_anon_split(page))
// 		goto out;
	
// 	BUG_ON(PageTransCompound(page));

// 	//TODO: 私有文件映射
// 	if (!PageAnon(page))
// 		goto out;


// 	/*
// 	 * We need the page lock to read a stable PageSwapCache in
// 	 * write_protect_page().  We use trylock_page() instead of
// 	 * lock_page() because we don't want to wait here - we
// 	 * prefer to continue scanning and merging different pages,
// 	 * then come back to this page when it is unlocked.
// 	 */
// 	if (!trylock_page(page))
// 		goto out;
// 	/*
// 	 * If this anonymous page is mapped only here, its pte may need
// 	 * to be write-protected.  If it's mapped elsewhere, all of its
// 	 * ptes are necessarily already write-protected.  But in either
// 	 * case, we need to lock and check page_count is not raised.
// 	 */
// 	if (write_protect_page(vma, page, &orig_pte) == 0) {
// 		if (is_page_full_zero(page)){
// 			err = replace_page(vma, page, zero_page, orig_pte);
// 		}
// 	}


// 	if ((vma->vm_flags & VM_LOCKED) && !err) {
// 		munlock_vma_page(page);
// 		if (!PageMlocked(zero_page)) {
// 			unlock_page(page);
// 			lock_page(zero_page);
// 			mlock_vma_page(zero_page);
// 			page = zero_page;		/* for final unlock */
// 		}
// 	}
// out_unlock:
// 	unlock_page(page);
// out:
// 	if(err == 0){			// err==0代表操作成功
// 		++pksm_pages_sharing;
// 		return true;	// 反向映射模块定义的标志字段，代表此次操作成功，继续遍历
// 	}else{
// 		return false;	// 此次操作失败，反向映射遍历终止
// 							//? 只是一次失败就需要终止整个遍历过程吗？
// 	}
// }

// TODO:KSM中merge_ksm/two_page中，在merge_one调用之前会调用down_read(mmap_sem)
/*
 * pksm中将指向一个page的pte指向另一个kpage的函数
 * 是pksm_try_to_merge_one_page在反向映射机制上调用的单体操作
 */
static bool try_to_merge_one_page(struct page *page, struct vm_area_struct *vma,
		     unsigned long address, void *arg)
{
	struct page *kpage = ((struct rmap_process_wrapper*)arg)->kpage;
	struct pksm_hash_node *pksm_hash_node = ((struct rmap_process_wrapper*)arg)->pksm_hash_node;
	struct pksm_rmap_item *pksm_rmap_item;	

	pte_t orig_pte = __pte(0);
	int err = -EFAULT;

	if (page == kpage)			/* ksm page forked */
		return 0;

	if(ksm_test_exit(vma->vm_mm)){
		return true;
	}
	

	// 这里是ksm用于判断这个虚地址空间是否应该参与merge的标志
	// pksm里不用，直接全部merge
	// if (!(vma->vm_flags & VM_MERGEABLE))
	// 	goto out;

	
	if (PageTransCompound(page) && page_trans_compound_anon_split(page))
		goto out;
	
	BUG_ON(PageTransCompound(page));

	//TODO: 私有文件映射
	if (!PageAnon(page))
		goto out;


	/*
	 * We need the page lock to read a stable PageSwapCache in
	 * write_protect_page().  We use trylock_page() instead of
	 * lock_page() because we don't want to wait here - we
	 * prefer to continue scanning and merging different pages,
	 * then come back to this page when it is unlocked.
	 */
	if (!trylock_page(page))
		goto out;
	/*
	 * If this anonymous page is mapped only here, its pte may need
	 * to be write-protected.  If it's mapped elsewhere, all of its
	 * ptes are necessarily already write-protected.  But in either
	 * case, we need to lock and check page_count is not raised.
	 */
	if (write_protect_page(vma, page, &orig_pte) == 0) {
		if (!kpage) {
			set_page_stable_node(page, pksm_hash_node);	// 因为我们此时已经知道hash_node了，所以直接set到page里
														// 但是原则上属于破坏了我们正在循环遍历的结构，不知道会不会出问题
			mark_page_accessed(page);
			err = 0;
		} else{
			if (pages_identical(page, kpage)){
				err = replace_page(vma, page, kpage, orig_pte);
			}
		}
	}


	if ((vma->vm_flags & VM_LOCKED) && kpage && !err) {
		munlock_vma_page(page);
		if (!PageMlocked(kpage)) {
			unlock_page(page);
			lock_page(kpage);
			mlock_vma_page(kpage);
			page = kpage;		/* for final unlock */
		}
	}

	if(err == 0){
		pksm_rmap_item = alloc_pksm_rmap_item();

		pksm_rmap_item->anon_vma = vma->anon_vma;
		pksm_rmap_item->mm = vma->vm_mm;
		pksm_rmap_item->address = address;

		//? 后来加上
		get_anon_vma(vma->anon_vma);

		hlist_add_head( &(pksm_rmap_item->hlist), &(pksm_hash_node->rmap_list));
	}

	unlock_page(page);
out:
	if(err == 0){			// err==0代表操作成功
		++pksm_pages_sharing;
		return true;	// 反向映射模块定义的标志字段，代表此次操作成功，继续遍历
	}else{
		return false;	// 此次操作失败，反向映射遍历终止
							//? 只是一次失败就需要终止整个遍历过程吗？
	}
}

// 模仿的rmap.c/try_to_unmap函数搞得rwc，不想多include了，就额外实现一个
static int pksm_page_not_mapped(struct page *page)
{
	return !page_mapped(page);
};

#ifdef SYST_NOINLINE
static noinline int pksm_try_to_merge_zero_page(struct page *page)
#else
static int pksm_try_to_merge_zero_page(struct page *page)
#endif
{
	int ret;

	++pksm_zero_merged;

	struct rmap_walk_control rwc = {
		.rmap_one = try_to_merge_zero_page,
		// .arg = (void *)(empty_pksm_zero_page),
		.done = pksm_page_not_mapped,
		.anon_lock = page_lock_anon_vma_read,
	};

	rmap_walk(page, &rwc);	//? 这里是否需要lock存疑，以前是lock的，所以继续lock

#ifdef SCAN_STEP_CNT
	switch(pksm_cur_scan_step){
		case 3: pksm_scan_step_cnts[0]+=1; break;
		case 7: pksm_scan_step_cnts[1]+=1; break;
		case 17: pksm_scan_step_cnts[2]+=1; break;
		case 29: pksm_scan_step_cnts[3]+=1; break;
		case 41: pksm_scan_step_cnts[4]+=1; break;
		default: printk(KERN_ALERT "PKSM : pksm_cur_scan_step wrong\n"); break;
	}

	if(pksm_scan_status){
		pksm_scan_step_pervage_cnts[5] += 1;
	}else{
		switch(pksm_cur_scan_step){
			case 3: pksm_scan_step_pervage_cnts[0]+=1; break;
			case 7: pksm_scan_step_pervage_cnts[1]+=1; break;
			case 17: pksm_scan_step_pervage_cnts[2]+=1; break;
			case 29: pksm_scan_step_pervage_cnts[3]+=1; break;
			case 41: pksm_scan_step_pervage_cnts[4]+=1; break;
			default: printk(KERN_ALERT "PKSM : pksm_cur_scan_step wrong\n"); break;
		}
	}
#endif

	return !page_mapcount(page) ? 0 : 1;
		
}

/*
 * pksm中实际merge两个page的函数
 * 是try_to_merge_one_page的反向映射迭代入口
 * 成功则返回0
 * #define SWAP_SUCCESS	0
 * #define SWAP_AGAIN	1
 * #define SWAP_FAIL	2
 * #define SWAP_MLOCK	3
 */
static int pksm_try_to_merge_one_page(struct page *page, struct page *kpage, struct pksm_hash_node *pksm_hash_node)
{
	// TODO: 暂时先不用kalloc
	struct rmap_process_wrapper rmap_process_wrapper = {pksm_hash_node, kpage};
	int ret;

	// TODO: 下面的两个分支里存在代码冗余

	if(kpage != NULL){	// 对应真实归并的情况
		// 因为这里的rmap处理逻辑和unmap基本相同
		// 只是增加了释放映射后重映射的操作
		// 因此基本上采用了try_to_unmap的结构
		struct rmap_walk_control rwc = {
			.rmap_one = try_to_merge_one_page,
			.arg = (void *)(&rmap_process_wrapper),
			.done = pksm_page_not_mapped,
			.anon_lock = page_lock_anon_vma_read,
		};

		// ret = rmap_walk(page, &rwc);
		rmap_walk_locked(page, &rwc);	//? 这里是否需要lock存疑，以前是lock的，所以继续lock

		return !page_mapcount(page) ? 0 : 1;
	}else{	// 对应将page置为ksm的情况
		/* TODO: 原则上这里只用对一个vma操作一下就可以了，但是我不会，所以就先这样
		 * 使用反向映射机制主要是为了得到vma来调用write_protect  
		 */
		struct rmap_walk_control rwc = {
			.rmap_one = try_to_merge_one_page,
			.arg = (void *)(&rmap_process_wrapper),
			.done = PagePksm,	// 当这个页面已经成为PKSM页面后就终止反向映射遍历过程
								//? 很奇怪，一个有多个反向映射的页该怎么处理？
								//? 再KSM中就是直接把对应的vma->anon_vma赋给rmap_item对象，然后就可以直接原地设置page为KSM页了
								//? 可能anon_vma本身就是一个全局结构吧
								//? 那这样子的话后续merge_pksm的操作不是会导致anon_vma的重复添加吗 
			.anon_lock = page_lock_anon_vma_read,
		};

		rmap_walk_locked(page, &rwc);

		return PagePksm(page) ? 0 : 1;
	}

	
}

/**
 * 这个函数是额外添加的，因为在下一步里需要hash_node这个参数
 * 但是设置pksm和归并pksm时的hash_node来源不同（kpage参数也不同），强行搞成一个函数没有必要
 * 在这一步就可以完全获得hash_node和kpage，下一步的merge_one_page就不需要再拆分
 */
#ifdef SYST_NOINLINE
static noinline int try_to_set_this_pksm_page(struct page_slot *page_slot, 
					  struct page *page, struct pksm_hash_node *pksm_hash_node)
#else
static int try_to_set_this_pksm_page(struct page_slot *page_slot, 
					  struct page *page, struct pksm_hash_node *pksm_hash_node)
#endif
{
	int err = -EFAULT;
	
	if(pksm_test_exit(page_slot)){
		goto out;
	}

	if(PagePksm_inline(page)){
		goto out;
	}

	err = pksm_try_to_merge_one_page(page, NULL, pksm_hash_node);
	if(err){
		goto out;
	}

	page_slot->mapcount = page_mapcount(page);
	remove_node_from_hashlist(page_slot);

	// 一来要确保这一步之后page就是一个完整的pksm_page
	// 二来之后没必要再单独搞一个hash_node的完善操作
	// 因此在这里直接设置掉
	// 原则上这里应该不需要锁
	pksm_hash_node->kpfn = page_to_pfn(page);

	++pksm_pages_shared;

out:
	return err;
}

#ifdef SYST_NOINLINE
static noinline int try_to_merge_with_pksm_page(struct page_slot *page_slot, 
					  struct page *page, struct page *kpage)
#else
static int try_to_merge_with_pksm_page(struct page_slot *page_slot, 
					  struct page *page, struct page *kpage)
#endif
{
	int err = -EFAULT;
	
	if(pksm_test_exit(page_slot)){
		goto out;
	}

	err = pksm_try_to_merge_one_page(page, kpage, page_stable_node(kpage));
	if(err){
		goto out;
	}

	/*
	 * 没必要实现在这里
	 * 1、当发生stable归并时，page_slot对应cur_slot，此前已经remove过
	 * 2、当发生unstable归并时，page_slot对应table_slot，移出和无效化应紧密结合
	 */

	// remove_node_from_hashlist(page_slot);

	++pksm_pages_merged;

#ifdef SCAN_STEP_CNT
	switch(pksm_cur_scan_step){
		case 3: pksm_scan_step_cnts[0]+=1; break;
		case 7: pksm_scan_step_cnts[1]+=1; break;
		case 17: pksm_scan_step_cnts[2]+=1; break;
		case 29: pksm_scan_step_cnts[3]+=1; break;
		case 41: pksm_scan_step_cnts[4]+=1; break;
		default: printk(KERN_ALERT "PKSM : pksm_cur_scan_step wrong\n"); break;
	}

	if(pksm_scan_status){
		pksm_scan_step_pervage_cnts[5] += 1;
	}else{
		switch(pksm_cur_scan_step){
			case 3: pksm_scan_step_pervage_cnts[0]+=1; break;
			case 7: pksm_scan_step_pervage_cnts[1]+=1; break;
			case 17: pksm_scan_step_pervage_cnts[2]+=1; break;
			case 29: pksm_scan_step_pervage_cnts[3]+=1; break;
			case 41: pksm_scan_step_pervage_cnts[4]+=1; break;
			default: printk(KERN_ALERT "PKSM : pksm_cur_scan_step wrong\n"); break;
		}
	}
#endif

out:
	return err;
}

static struct page * pksm_try_to_merge_two_pages(struct page_slot *page_slot, struct page *page, 
							struct page_slot *table_page_slot, struct page *table_page, struct pksm_hash_node *pksm_hash_node)
{

	int err = -EFAULT;

	err = try_to_set_this_pksm_page(page_slot, page, pksm_hash_node);
	if (!err) {
		err = try_to_merge_with_pksm_page(table_page_slot, table_page, page);
		// try_to_merge_with_pksm_page(table_page_slot, table_page, page);

		/*
		 * If that fails, we have a ksm page with only one pte
		 * pointing to it: so break it.
		 */
		if (err){
			// 这里额外传入hash_node是因为此时page_slot->page_item必为空，因为在cmp_merge中首先将cur_page从table中移出
			break_cow(page_slot, pksm_hash_node);
		}else{
			page_slot->mapcount = page_mapcount(page);
		}
	}

	return err ? NULL : page;
}

#ifdef SYST_NOINLINE
static noinline struct page *unstable_hash_search_insert(struct page_slot *page_slot, struct page *page, 
								unsigned int entryIndex, uint32_t partial_hash, struct page_slot **table_page_slot)
#else
static struct page *unstable_hash_search_insert(struct page_slot *page_slot, struct page *page, 
								unsigned int entryIndex, uint32_t partial_hash, struct page_slot **table_page_slot)
#endif
{
	struct pksm_hash_node *unstable_node;
	struct hlist_node *nxt;
	struct page *hash_page;
	int ret;
	int cnt_bucket = 0;
	int stale_bucket = 0;
	int partial_hash_skip = 0;
	unsigned int cur_entryIndex;
	uint32_t new_partial_hash;

	unstable_cnt_bucket = 0;

	// printk("PKSM : unstable_hash_search_insert evoked : entryIndex = %u\n", entryIndex);


	hlist_for_each_entry_safe(unstable_node, nxt, &(unstable_hash_table[entryIndex]), hlist){
		// printk("PKSM : unstable_hash_search_insert : unstable_node:%p\n", unstable_node);

		// get_page是通过检查page->mapping的映射的方式获取页面
		// 但是在unstable_table中并不需要修改page的映射
		// ksm中这里使用get_mergeable_page通过mm+address获得对应的page
		// 所以这里要不也直接使用page好了
		// 注意这里使用了follow_page(vma, addr, FOLL_GET)，执行了一次get_page
		// 所以外面会有一次put_page
		// hash_page = get_pksm_page(unstable_node, false);

		if(pksm_test_exit(unstable_node->page_slot)){
			// printk("PKSM : unstable_hash_search_insert : exit item: %p, slot: %p\n", unstable_node, unstable_node->page_slot);
			// hlist_del(&(unstable_node->hlist)); 
			// __hlist_del(&(unstable_node->hlist)); 
			++stale_bucket;
			continue;
		}

		hash_page = unstable_node->page_slot->physical_page;

		if(!hash_page){
			// printk("PKSM : cmp end notcount\n");

			continue;
		}


		// printk("PKSM : cmp start\n");

		// if(partial_hash != unstable_node->page_slot->partial_hash){
		// 	++partial_hash_skip;
		// 	// if(memcmp_pages(page, hash_page) == 0){
		// 	// 	printk("PKSM : error partial-hash wrong\n");
		// 	// }
		// 	// printk("PKSM : cmp end partial_hash\n");

		// 	continue;
		// }


		get_page(hash_page);
		++cnt_bucket;


		++unstable_cnt_bucket;
		// printk("PKSM : unstable_hash_search_insert : get_page: %p\n", hash_page);
		ret = memcmp_pages(page, hash_page);

		if (ret == 0){
			// printk("PKSM : cmp end same\n");

			// printk("PKSM : unstable_hash_search_insert found at valid: %d, stale: %d, skip: %d \n", cnt_bucket, stale_bucket, partial_hash_skip);
			*table_page_slot = unstable_node->page_slot;
			return hash_page;
		}

		// printk("PKSM : cmp end\n");


		put_page(hash_page);
	}

	// printk("PKSM : unstable_hash_search_insert : not-found with length valid: %d, stale: %d, skip: %d \n", cnt_bucket, stale_bucket, partial_hash_skip);

	// if(page_slot->page_item == NULL){
	if(page_slot_not_in_hash_table(page_slot)){
		page_slot->page_item = alloc_hash_node();
	}else{
		printk("PKSM : bug occur, unstable_hash_search_insert with page_slot->page_item != NULL\n");
		remove_node_from_hashlist(page_slot);
	}

	page_slot->page_item->kpfn = page_to_pfn(page);

	// printk("PKSM : unstable_hash_search_insert : slot: %p, item: %p, kpfn: %lu\n", page_slot, page_slot->page_item, page_slot->page_item->kpfn);

	INIT_HLIST_HEAD(&(page_slot->page_item->rmap_list));

	page_slot->page_item->page_slot = page_slot;

	// 因为entryindex发生变化的可能性很小
	// printk("PKSM : partial_hash start\n");
	// cur_entryIndex = calc_hash(page, &new_partial_hash) & PAGE_HASH_MASK;	
	// printk("PKSM : partial_hash end\n");

	page_slot->partial_hash = partial_hash;

	// printk("PKSM : unstable_hash_search_insert : entryIndex %u -> %u\n", entryIndex, cur_entryIndex);

	hlist_add_head(&(page_slot->page_item->hlist), &(unstable_hash_table[entryIndex]));

	return NULL;
}

#ifdef SYST_NOINLINE
static noinline struct page *stable_hash_search(struct page *page, unsigned int entryIndex, uint32_t partial_hash)
#else
static struct page *stable_hash_search(struct page *page, unsigned int entryIndex, uint32_t partial_hash)
#endif
{
	struct pksm_hash_node *stable_node;
	struct hlist_node *nxt;
	struct page *hash_page;
	int ret;
	// int cnt_bucket = 0;
	// int stale_bucket = 0;
	// int partial_hash_skip = 0;

	stable_cnt_bucket = 0;

	// printk("PKSM : stable_hash_search evoked : entryIndex = %u\n", entryIndex);

	stable_node = page_stable_node(page);

	// printk("PKSM : stable_hash_search : page: %p, node: %p\n", page, stable_node);

	if (stable_node) {			/* ksm page already */
		get_page(page);
		return page;
	}

	hlist_for_each_entry_safe(stable_node, nxt, &(stable_hash_table[entryIndex]), hlist){

		// if(stable_node->page_slot->partial_hash != partial_hash){
		// 	continue;
		// }
		
		hash_page = get_pksm_page(stable_node, false);

		// ++cnt_bucket;

		if(!hash_page){
			// printk("PKSM : cmp end not_count\n");

			continue;
		}


		// printk("PKSM : stable_hash_search : get_page: %p\n", hash_page);
		
		++stable_cnt_bucket;
		ret = memcmp_pages(page, hash_page);

		if (ret == 0){
			// printk("PKSM : cmp end same\n");
			// printk("PKSM : stable_hash_search found at valid: %d, stale: %d, skip: %d \n", cnt_bucket, stale_bucket, partial_hash_skip);
			return hash_page;
		}

		// printk("PKSM : cmp end\n");


		put_page(hash_page);
	}
	// printk("PKSM : stable_hash_search : not-found with length valid: %d, stale: %d, skip: %d \n", cnt_bucket, stale_bucket, partial_hash_skip);
	return NULL;
}

// TODO: fail state
static void stable_hash_insert(struct page_slot *kpage_slot, struct page *kpage, struct pksm_hash_node *pksm_hash_node){
	u32 cur_hash;
	unsigned int entryIndex;
	uint32_t partial_hash;

	if(page_slot_in_hash_table(kpage_slot)){
		printk(KERN_ALERT "PKSM : bug occur, stable_hash_insert with kpage_slot->page_item != NULL\n");
		remove_node_from_hashlist(kpage_slot);
	}

	kpage_slot->page_item = pksm_hash_node;
	pksm_hash_node->page_slot = kpage_slot;


	// 重新计算当前页面的哈希值
	cur_hash = calc_hash(kpage, &partial_hash);
	entryIndex = cur_hash & PAGE_HASH_MASK;
	kpage_slot->partial_hash = partial_hash;

	hlist_add_head(&(pksm_hash_node->hlist), &(stable_hash_table[entryIndex]));
}

void merge_pervade(struct page_slot *slot_1, struct page_slot *slot_2){
	unsigned long pfn_1, pfn_2;
	struct page *page_1;
	struct page *page_2;

	pfn_1 = page_to_pfn(slot_1->physical_page)+1;
	pfn_2 = page_to_pfn(slot_2->physical_page)+1;

	page_1 = pfn_to_page(pfn_1);
	page_2 = pfn_to_page(pfn_2);

	// perf_break_point(4, 0);

	if(!(PageAnon(page_1)&&PageAnon(page_2))){
		return;
	}
	// perf_break_point(4, 1);

	if(!(get_page_slot(page_1)&&get_page_slot(page_2))){
		return;
	}
	// perf_break_point(4, 2);

	if(!pages_identical(page_1, page_2)){
		return;
	}
	// perf_break_point(4, 3);

}

/*
 * 针对当前的page_slot对象对应的page结构寻找可以归并的归宿
 */
static void pksm_cmp_and_merge_page(struct page_slot *cur_page_slot)
{
	struct page *cur_page = cur_page_slot->physical_page;
	u32 cur_hash;
	unsigned int entryIndex;
	struct page *kpage;
	struct page *unstable_page;
	struct pksm_hash_node *hash_node;
	int err;
	struct page_slot *table_page_slot = NULL;
	unsigned long map_log;
	uint32_t partial_hash;

	// perf_break_point(3, 0);

	if(unlikely(pksm_test_exit(cur_page_slot))){	//当前page已经离开
		remove_node_from_hashlist(cur_page_slot);
		// perf_break_point(3, 1);
		return;
	}else if(unlikely(PagePksm_inline(cur_page))){	// 如果当前page是pksm页，直接跳过
		map_log = page_mapcount(cur_page);
		if(unlikely(map_log < cur_page_slot->mapcount)){
			pksm_pages_sharing -= (cur_page_slot->mapcount - map_log);
			cur_page_slot->mapcount = map_log;
		}
		// perf_break_point(3, 2);
		return;
	}else{

		// * 不由分说先默认此次归并失败，这样可以避免之后的分支操作
		// * 如果之后发现此次归并成功，再减掉
		

		cur_hash = calc_hash(cur_page, &partial_hash);

		cur_page_slot->partial_hash = partial_hash;

		// * 太早remove可能会导致ksm_exit中的错误释放（easy_free）
		remove_node_from_hashlist_not_null(cur_page_slot);

		if(cur_hash == zero_hash){
			err = pksm_try_to_merge_zero_page(cur_page);
			if (!err){
				pksm_cur_cont_unmerged_pages = 0;
				++pksm_cur_merged_pages;
				++pksm_scan_status;
				return;
			}
		}


		entryIndex = cur_hash & PAGE_HASH_MASK;
		// perf_break_point(3, 3);

		// 在stable表中寻找归并页
		kpage = stable_hash_search(cur_page, entryIndex, partial_hash);
		
		if(unlikely(kpage == cur_page)){	// 已经是pksmpage了
			put_page(kpage);
			// printk("PKSM : pksm_cmp_and_merge_page : page already stable\n");
			// perf_break_point(3, 4);
			return;
		}
		// perf_break_point(3, 5);
		// 去除残留这一步在之前已经做了，所以不用做了
		// remove_node_from_tree(page_slot->page_item); 
		if(kpage){
			err = try_to_merge_with_pksm_page(cur_page_slot, cur_page, kpage);
			// printk("PKSM : pksm_cmp_and_merge_page : try_to_merge_with_pksm_page(%p, %p) finish\n", cur_page, kpage);

			if(!err){
				table_page_slot = get_page_slot(kpage);
				if(table_page_slot){
					table_page_slot->mapcount = page_mapcount(kpage);
				}

				// page 成功 merge 到一个pksmpage
				// cur_page_slot->invalid = true;
				pksm_cur_cont_unmerged_pages = 0;
				++pksm_cur_merged_pages;
				++pksm_scan_status;
			}else{
				++pksm_cur_cont_unmerged_pages;
				++pksm_cur_unmerged_pages;
				pksm_scan_status >>= 1;
			}
			put_page(kpage);

			// perf_break_point(3, 6);
			return;
		}
		// perf_break_point(3, 7);

		// 在unstable表中寻找归并页
		// ? 传统方法里先归并，再使用虚拟空间信息创建stable node，并加入page的mapping字段
		// ? 但是pksm中只有归并时能看到虚拟地址，需要已有stable_node -> 需要调整顺序
		// ? 调整顺序后可能会带来正确性检查问题，到时候再说
		// ? 但是在归并的过程中会使用到page的原mapping信息，因此不能直接修改
		// ? 可以先生成一个stable_node结构，然后通过传参的形式层层处理，最后在外面再加入哈希桶
		// ? 当然也可以先把这个node挂载page_slot上，但是这样会造成不一致性，暂时先不这么搞

		// printk("PKSM : partial_hash start\n");
		// partial_hash = calc_partial_hash(cur_page);
		// // printk("PKSM : partial_hash end\n");

		// if((cur_page_slot->partial_hash != partial_hash)){
		// 	// printk("PKSM : pksm_cmp_and_merge_page : volatile %u -> %u\n", cur_page_slot->partial_hash, partial_hash);
		// 	cur_page_slot->partial_hash = partial_hash;
		// 	// perf_break_point(3, 8);
		// 	return;
		// }

		// entryIndex = cur_hash & PAGE_HASH_MASK;
		// perf_break_point(3, 9);


		unstable_page = unstable_hash_search_insert(cur_page_slot, cur_page, entryIndex, partial_hash, &table_page_slot);
		// perf_break_point(3, 10);
		
		if(unstable_page){
			
			// merge_pervade(table_page_slot, cur_page_slot);

			hash_node = alloc_hash_node();
			if(unlikely(!hash_node)){
				printk(KERN_ALERT "PKSM : pksm_cmp_and_merge_page : unstable_hash_node alloc_fail");
			}

			hash_node->kpfn = page_to_pfn(cur_page);

			INIT_HLIST_HEAD(&(hash_node->rmap_list));

			kpage = pksm_try_to_merge_two_pages(cur_page_slot, cur_page, table_page_slot, unstable_page, hash_node);
			// 这是cur_page已经变成pksm_page了
			// printk("PKSM : pksm_cmp_and_merge_page : pksm_try_to_merge_two_pages finish\n");
			put_page(unstable_page);
			if (kpage) {

				// stable_hash_insert里需要计算这个page的哈希值，所以锁仍然不能去除
				lock_page(kpage);
				stable_hash_insert(cur_page_slot, kpage, hash_node);
				unlock_page(kpage);

				// invalid意味着页不再参与pksm->匿名页离开系统
				// TODO: 要将已经完成归并的pksm页移出扫描对象队列中，但不能粗暴地通过invalid位来设置
				// cur_page_slot->invalid = true;

				// table_page_slot可以设置为invalid，因为原则上它*应该*已经不再被映射了才对
				table_page_slot->invalid = true;

				// remove不一定要立即做，可能会对anon的操作产生影响
				// 事实上remove确实要立即做，但是会区分是否stable
				remove_node_from_hashlist(table_page_slot);

				pksm_cur_cont_unmerged_pages = 0;
				++pksm_cur_merged_pages;
				++pksm_scan_status;

				// if (!stable_node) {
				// 	break_cow();
				// }

				// printk("PKSM : pksm_cmp_and_merge_page : kpage: %p, table_slot: %p, invalid: %d\n", kpage, table_page_slot, table_page_slot->invalid);

				// ++pksm_page_shared;

			}else{
				++pksm_cur_cont_unmerged_pages;
				++pksm_cur_unmerged_pages;
				pksm_scan_status >>= 1;
				// free_all_rmap_item_of_node(hash_node);
				// free_hash_node(hash_node)
			}

			// perf_break_point(3, 11);
		}else{
			++pksm_cur_cont_unmerged_pages;
			++pksm_cur_unmerged_pages;
			pksm_scan_status >>= 1;
			// perf_break_point(3, 12);
		}

	}
}

static void calc_scan_step(unsigned long cur_stamp){
	unsigned long stamp_diff = pksm_scan.seqnr-cur_stamp;
	if(pksm_new_pages_inlist > 32768){ //128MB
	// if(pksm_new_pages_inlist > 32768‬){	//128MB
		pksm_cur_scan_step = pksm_scan_steps[4];
	}else{
		if(stamp_diff <= 10){
			pksm_cur_scan_step = pksm_scan_steps[pksm_step_level[stamp_diff]];
		}else{
			pksm_cur_scan_step = pksm_scan_steps[0];
		}
	}
}

#ifdef SYST_NOINLINE
static noinline struct page_slot *scan_get_next_page_slot(void)
#else
static struct page_slot *scan_get_next_page_slot(void)
#endif
{
	struct page_slot *cur_slot;
	struct page *cur_page;
	unsigned int remain_step;
	unsigned long irq_flags;

	if(list_empty(&(pksm_page_head.page_list))){
		return NULL;
	}

	if(pksm_scan_status){
		remain_step = 1;
	}else{
		remain_step = pksm_cur_scan_step;
	}

	// 原则上pksm_scan.page_slot对应的是下一个待扫描对象
	// slot对应当前扫描（处理）对象
	// 在下面的一段代码中，主要是获取并移动slot，所以会发生短暂的两者重合
	// 在next_page代码段中第一项工作就是移动pksm_scan.page_slot使两者重新分离
next_step:
	cur_slot = pksm_scan.page_slot;

	if(cur_slot == &pksm_page_head){
		// printk("PKSM : scan_get_next_page_slot CPU# %d try lock", smp_processor_id());
		spin_lock_irqsave(&pksm_pagelist_lock, irq_flags);
		// printk("PKSM : scan_get_next_page_slot CPU# %d acquire lock", smp_processor_id());

		pksm_scan.seqnr++;
		pksm_new_pages_inlist = 0;
		cur_slot = list_entry(cur_slot->page_list.next, struct page_slot, page_list);
		pksm_scan.page_slot = cur_slot;
		spin_unlock_irqrestore(&pksm_pagelist_lock, irq_flags);
		// printk("PKSM : scan_get_next_page_slot CPU# %d unlock", smp_processor_id());

		if(cur_slot == &pksm_page_head){
			return NULL;
		}
	}

 next_page:

	cur_page = cur_slot->physical_page;

	// printk("PKSM : scan_get_next_page_slot CPU# %d try lock", smp_processor_id());
	spin_lock_irqsave(&pksm_pagelist_lock, irq_flags);
	// printk("PKSM : scan_get_next_page_slot CPU# %d acquire lock", smp_processor_id());

	pksm_scan.page_slot = list_entry(pksm_scan.page_slot->page_list.next, struct page_slot, page_list);

	if(pksm_test_exit(cur_slot)){
		remove_from_page_slots_hash(cur_slot);
		// hash_del(&cur_slot->link);			//从page -> page_slot映射表中删除
		list_del(&cur_slot->page_list);
		spin_unlock_irqrestore(&pksm_pagelist_lock, irq_flags);
		// printk("PKSM : scan_get_next_page_slot CPU# %d unlock", smp_processor_id());

		remove_node_from_hashlist(cur_slot);
		free_page_slot(cur_slot);

	}else{
		spin_unlock_irqrestore(&pksm_pagelist_lock, irq_flags);
		// printk("PKSM : scan_get_next_page_slot CPU# %d unlock", smp_processor_id());

		remain_step -= 1;
		if(remain_step == 0){
			get_page(cur_slot->physical_page);
			// TODO: if(valid_pksm_page(cur_page)){
			return cur_slot;
			// } 
		}

	}

	goto next_step;

	// 即使碰到head也应该继续
	// if(cur_slot != &pksm_page_head){
	// 	goto next_page;
	// }
	
	return NULL;
}

// TODO: 使休眠时间与进程实际工作时间相关
static unsigned int get_time_to_sleep(void){
	// return (unsigned int) ((unsigned long long) pksm_thread_sleep_millisecs_base *
	//  		(unsigned long long) pksm_cur_unmerged_pages / 
	//  		(unsigned long long) pksm_cur_merged_pages);
	return pksm_thread_sleep_millisecs_base;
}

static noinline void pksm_do_scan(void)
{
	struct page_slot *page_slot;
	// struct page_slot *pre_slot = NULL;
	// pksm_cur_cont_unmerged_pages = 0;
	// // 默认为1，防止出现除零异常
	// pksm_cur_merged_pages = 1;
	// pksm_cur_unmerged_pages = 1;

	//TODO：这两个是否需要
	// get_page(empty_pksm_zero_page);

	 
	while ((pksm_cur_cont_unmerged_pages < pksm_cont_unmerged_pages_threshold) && ((pksm_cur_merged_pages+pksm_cur_unmerged_pages) < pksm_scaned_pages_threshold) && likely(!freezing(current))) {
	// while ((pksm_cur_cont_unmerged_pages < pksm_cont_unmerged_pages_threshold) && likely(!freezing(current))) {
		cond_resched();
		// perf_break_point(0, 0);
		page_slot = scan_get_next_page_slot();

		// perf_break_point(0, 1);
		if (unlikely(!page_slot))
			return;

		if(unlikely(page_slot == &pksm_page_head)){
			printk(KERN_ALERT "PKSM : bug occur get_next_slot return page_head");
			continue;
		}

		calc_scan_step(page_slot->add_stamp);

		// if(pre_slot != NULL && pre_slot == page_slot){
		// 	printk("PKSM : pksm_do_scan : same slot %p\n", page_slot);
		// 	return;
		// }

		// pre_slot = page_slot;

		pksm_cmp_and_merge_page(page_slot);
		// perf_break_point(0, 2);


		// TODO: 这里的put_page会进入mm子系统，重新获取pksm相关结构，浪费
		// if(is_page_full_zero(page_slot->physical_page)){
		// 	printk("PKSM : zero_merge, %d", page_ref_count(page_slot->physical_page))
		// }
		put_page(page_slot->physical_page);
		
		// if(page_ref_count(page_slot->physical_page) == 1){
			
		// 	put_page(page_slot->physical_page);
		// 	// perf_break_point(0, 3);
		// }else{
		// 	put_page(page_slot->physical_page);
		// 	// perf_break_point(0, 4);
		// }
	}

	pksm_thread_sleep_millisecs_real = get_time_to_sleep();
	pksm_last_merged_pages = pksm_cur_merged_pages;
	pksm_last_unmerged_pages = pksm_cur_unmerged_pages;
	if(pksm_thread_sleep_millisecs_real < pksm_thread_sleep_millisecs_low){
		pksm_thread_sleep_millisecs_real = pksm_thread_sleep_millisecs_low;
	}else if(pksm_thread_sleep_millisecs_real > pksm_thread_sleep_millisecs_high){
		pksm_thread_sleep_millisecs_real = pksm_thread_sleep_millisecs_high;
	}

	// put_page(empty_pksm_zero_page);

}

static int pksmd_should_run(void)
{
	// if((pksm_run & PKSM_RUN_MERGE) && !list_empty(&pksm_page_head.page_list)){
	// 	// printk("PKSM : pksmd_should_run : true\n");
	// 	return true;
	// }else{
	// 	// printk("PKSM : pksmd_should_run : false\n");
	// 	return false;
	// }

	return ((pksm_run & PKSM_RUN_MERGE) && !list_empty(&pksm_page_head.page_list));
	
}



static int pksm_scan_thread(void *nothing)
{
	set_freezable();
	set_user_nice(current, 5);

	while (!kthread_should_stop()) {
		mutex_lock(&pksm_thread_mutex);
		wait_while_offlining();
		if (pksmd_should_run()){
			if(pksm_cur_cont_unmerged_pages >= pksm_cont_unmerged_pages_threshold){
				pksm_cur_cont_unmerged_pages = 0;
			}
			// 默认为1，防止出现除零异常
			pksm_cur_merged_pages = 1;
			pksm_cur_unmerged_pages = 1;
			
			pksm_do_scan();
		}
		mutex_unlock(&pksm_thread_mutex);

		try_to_freeze();

		if (pksmd_should_run()) {
			schedule_timeout_interruptible(
				msecs_to_jiffies(pksm_thread_sleep_millisecs_real));
		} else {
			wait_event_freezable(pksm_thread_wait,
				pksmd_should_run() || kthread_should_stop());
		}
	}
	return 0;
}

int ksm_madvise(struct vm_area_struct *vma, unsigned long start,
		unsigned long end, int advice, unsigned long *vm_flags)
{
	switch(advice){
		case MADV_MERGEABLE:
			// printk("PKSM : ksm_madvise - MADV_MERGEABLE evoked\n");
			break;
		case MADV_UNMERGEABLE:
			// printk("PKSM : ksm_madvise - MADV_UNMERGEABLE evoked\n");
			break;
	}

	return 0;
}

// 会在memory.c/do_anonymous_page里调用 -> 处理缺页中断
// 会在memoty.c/wp_page_copy里调用 -> 处理cow
void pksm_new_anon_page(struct page *page, bool high_priority){
	struct page_slot *page_slot;
	int needs_wakeup;
	unsigned long irq_flags;
	// struct page_slot *pre_slot;

#ifdef MANUAL_PAGE_ADD
	if(pksm_run & PKSM_RUN_MERGE){
#endif

		page_slot = get_page_slot(page);
		if(unlikely(page_slot && (page_slot->invalid == false))){ // 为什么还要第二个条件，因为有可能已经not_easy exit了
				printk(KERN_ALERT "PKSM : pksm_new_anon_page wrong, page %p already in list slot %p\n", page, page_slot);
				return;
			// if(page_slot->invalid == true){
			// 	printk("PKSM : pksm_new_anon_page fake wrong, page %p in list slot %p\n", page, page_slot);
			// }else{
				// printk("PKSM : pksm_new_anon_page wrong, page %p already in list slot %p\n", page, page_slot);
				// return;
			// }
		}

		page_slot = alloc_page_slot();
		if(unlikely(page_slot == NULL)){
			printk(KERN_ALERT "PKSM : pksm_new_anon_page wrong, page_slot allocate fail, page: %p\n", page);
			return;
		}

		page_slot->mapcount = 0;
		page_slot->partial_hash = 0;
		page_slot->physical_page = page;
		page_slot->invalid = false;
		page_slot->page_item = NULL;	// 这个字段是否为NULL代表了这个page是否已经纳入pksm系统
										// 所以在初始化的时候确保他时NULL很重要
		page_slot->add_stamp = pksm_scan.seqnr;

		needs_wakeup = list_empty(&pksm_page_head.page_list);
		
		// printk("PKSM : pksm_new_anon_page CPU# %d try lock", smp_processor_id());
		spin_lock_irqsave(&pksm_pagelist_lock, irq_flags);
		// printk("PKSM : pksm_new_anon_page CPU# %d acquire lock", smp_processor_id());

		insert_into_page_slots_hash(page, page_slot);
		++pksm_new_pages_inlist;

		if (pksm_run & PKSM_RUN_UNMERGE)
			list_add_tail(&page_slot->page_list, &pksm_page_head.page_list);
		else{
			if(likely(high_priority)){
				list_add(&page_slot->page_list, &pksm_page_head.page_list);
				// list_add_tail(&page_slot->page_list, &pksm_page_head.page_list);
				// list_add_tail(&page_slot->page_list, &pksm_scan.page_slot->page_list);
				// list_add(&page_slot->page_list, &pksm_scan.page_slot->page_list);
			}else{
				list_add(&page_slot->page_list, &pksm_page_head.page_list);
				// list_add_tail(&page_slot->page_list, &pksm_page_head.page_list);
				// list_add_tail(&page_slot->page_list, &pksm_scan.page_slot->page_list);
			}

			// pre_slot = list_prev_entry(page_slot, page_list);
		}
			
		spin_unlock_irqrestore(&pksm_pagelist_lock, irq_flags);
		// printk("PKSM : pksm_new_anon_page CPU# %d unlock", smp_processor_id());

		// ? 在ksm里把一个进程加入ksm系统之后会增加其引用计数
		// 在pksm中是否需要同步增加其引用计数
		// atomic_inc(&mm->mm_count);

		if (needs_wakeup){
			wake_up_interruptible(&pksm_thread_wait);
		}else{

		}
#ifdef MANUAL_PAGE_ADD
	}else{
	}
#endif

}

void __pksm_exit(struct page *page)
{
	struct page_slot *page_slot;
	int easy_to_free = 0;

	// perf_break_point(1, 0);

	/*
	 * This process is exiting: if it's straightforward (as is the
	 * case when ksmd was never running), free mm_slot immediately.
	 * But if it's at the cursor or has rmap_items linked to it, use
	 * mmap_sem to synchronize with any break_cows before pagetables
	 * are freed, and leave the mm_slot on the list for ksmd to free.
	 * Beware: ksm may already have noticed it exiting and freed the slot.
	 */

#ifdef MANUAL_PAGE_ADD
	if(pksm_run & PKSM_RUN_MERGE){
#endif
		//TODO: 这个函数本来就会在softirq中运行，再屏蔽一次不知道会不会有问题
		// printk("PKSM : __pksm_exit CPU# %d try lock", smp_processor_id());
		spin_lock(&pksm_pagelist_lock);
		// printk("PKSM : __pksm_exit CPU# %d acquire lock", smp_processor_id());
		// perf_break_point(1, 1);

		page_slot = get_page_slot(page);
		// perf_break_point(1, 2);

		if (page_slot && pksm_scan.page_slot != page_slot) {
			page_slot->invalid = true;		//把当前page_slot标记为无效	
											//原本这个操作只在not_easy的情况下进行，但是考虑到多线程同步的问题放到外面可能比较好
			if (page_slot->page_item == NULL) {	// 如果page_slot此使没有加入stable/unstable table
				remove_from_page_slots_hash(page_slot);
				// hash_del(&page_slot->link);			//从page -> page_slot映射表中删除
				list_del(&page_slot->page_list);	//从page_slot的list中删除
				easy_to_free = 1;	
				// perf_break_point(1, 3);	
				if(page_slot->add_stamp == pksm_scan.seqnr){
					--pksm_new_pages_inlist;
				}
			} else {
				/*
				 * 把工作延后到scan过程中有两个原因：
				 * 1、针对not_easy的情况，有些操作（比如释放hashtable对象）不需要持有锁
				 * 2、exit过程会占用用户程序的运行时间
				 * 
				 * ps.仔细一想，理由一是不成立的，因为可以想slot_free一样在尾部不持有所的情况下进行
				 */
				list_move(&page_slot->page_list,	//现在只把他移动到遍历链表的下一个
					&pksm_scan.page_slot->page_list);		//以后可以根据优先级队列的设计进行适配
				// page_slot->invalid = true;		//把当前page_slot标记为无效	
				// perf_break_point(1, 4);
			}
		}else{
			// perf_break_point(1, 5);
		}

		spin_unlock(&pksm_pagelist_lock);
		// printk("PKSM : __pksm_exit CPU# %d unlock", smp_processor_id());

		// remove_from_page_slots_hash(page_slot);
		
		if (easy_to_free) {
			free_page_slot(page_slot);
		} else if (page_slot) {
			//TODO：要做什么？
		}
#ifdef MANUAL_PAGE_ADD
	}else{

	}
#endif
	// perf_break_point(1, 6);
}

struct page *ksm_might_need_to_copy(struct page *page,
			struct vm_area_struct *vma, unsigned long address)
{
	struct anon_vma *anon_vma = page_anon_vma(page);
	struct page *new_page;

	if (PageKsm(page)) {
		if (page_stable_node(page) &&
		    !(pksm_run & PKSM_RUN_UNMERGE))
			return page;	/* no need to copy it */
	} else if (!anon_vma) {
		return page;		/* no need to copy it */
	} else if (anon_vma->root == vma->anon_vma->root &&
		 page->index == linear_page_index(vma, address)) {
		return page;		/* still no need to copy it */
	}
	if (!PageUptodate(page))
		return page;		/* let do_swap_page report the error */

	new_page = alloc_page_vma(GFP_HIGHUSER_MOVABLE, vma, address);
	if (new_page) {
		copy_user_highpage(new_page, page, address, vma);

		SetPageDirty(new_page);
		__SetPageUptodate(new_page);
		__SetPageLocked(new_page);
	}

	return new_page;
}

// 我也不知道为什么会重复写这么一个函数
// static inline bool mm_test_exit(struct mm_struct *mm)
// {
// 	return atomic_read(&mm->mm_users) == 0;
// }


/*
 * 这个函数用来实现针对ksm页的反向映射机制，在rmap.c/rmap_walk中被调用主力pageKsm(page)为真的情况下被使用
 * 这些函数的目的是为了实现：给定一个page结构，针对所有映射它的虚拟页面进行操作
 * 众所周知，原则上多个pte映射一个page的情况并不自然存在
 * 针对匿名页面，仅有fork和ksm
 * 前者可以通过自然的反向映射进行组织，利用相应结构遍历所有虚拟页（见rmap.c/rmap_walk_anon）
 * 后者则需要自行实现一套 物理->逻辑 的映射方式用于实现相同的功能
 * 在原本的KSM中，通过 page->stable_node->rmap_item->vma 的方式实现
 * 但是在PKSM中，这样的反向映射关系好像没法记录
 * 
 * 有一个方法：
 * 继续使用rmap_item，但是创建时机不同
 * 在merge_one_page那里针对每一个 待归并页面反向映射到的vma创建rmap_item 然后后面继续一致操作
 * 
 * 但是这样会增加额外的复杂度，而且我觉得（我猜）针对PKSM页进行反向映射的机会并不多（应该）
 * 因为首先在PKSM系统中，不会对一个已经是PKSM页面的页进行处理
 * 然后再内存规整和swap的时候应该（好像、大概，我没看过）会避免对PKSM页面的操作
 * 所以暂时先把这个函数挂着，如果到时候出了问题再加入
 */

/*
 * 采用了上面的方法
 */

void rmap_walk_ksm(struct page *page, struct rmap_walk_control *rwc)
{
	struct pksm_hash_node *pksm_hash_node;
	struct pksm_rmap_item *pksm_rmap_item;
	int search_new_forks = 0;

	// printk("PKSM : rmap_walk_ksm called\n");

	if(unlikely(page = ZERO_PAGE(0))){
		printk(KERN_ALERT "PKSM : bug occur, rmap_zero");
	}


	VM_BUG_ON_PAGE(!PageKsm(page), page);

	/*
	 * Rely on the page lock to protect against concurrent modifications
	 * to that page's node of the stable tree.
	 */
	VM_BUG_ON_PAGE(!PageLocked(page), page);

	pksm_hash_node = page_stable_node(page);
	if (!pksm_hash_node)
		return;
again:
	hlist_for_each_entry(pksm_rmap_item, &pksm_hash_node->rmap_list, hlist) {
		struct anon_vma *anon_vma = pksm_rmap_item->anon_vma;
		struct anon_vma_chain *vmac;
		struct vm_area_struct *vma;

		cond_resched();
		anon_vma_lock_read(anon_vma);
		anon_vma_interval_tree_foreach(vmac, &anon_vma->rb_root,
					       0, ULONG_MAX) {
			cond_resched();
			vma = vmac->vma;

			// ! 这里处理在反向映射的时候某个进程已经退出的情况，作为pksm的页和反向映射的进程力度不一致的权宜之计
			if(ksm_test_exit(vma->vm_mm))
				continue;

			if (pksm_rmap_item->address < vma->vm_start ||
			    pksm_rmap_item->address >= vma->vm_end)
				continue;
			/*
			 * Initially we examine only the vma which covers this
			 * rmap_item; but later, if there is still work to do,
			 * we examine covering vmas in other mms: in case they
			 * were forked from the original since ksmd passed.
			 */
			if ((pksm_rmap_item->mm == vma->vm_mm) == search_new_forks)
				continue;

			if (rwc->invalid_vma && rwc->invalid_vma(vma, rwc->arg))
				continue;

			rwc->rmap_one(page, vma,
					pksm_rmap_item->address, rwc->arg);
			if (!rwc->rmap_one(page, vma, pksm_rmap_item->address, rwc->arg)) {
				anon_vma_unlock_read(anon_vma);
				goto out;
			}
			if (rwc->done && rwc->done(page)) {
				anon_vma_unlock_read(anon_vma);
				goto out;
			}
		}
		anon_vma_unlock_read(anon_vma);
	}
	if (!search_new_forks++)
		goto again;
out:
	return;
}

#ifdef CONFIG_MIGRATION
// TODO: 暂时不杀 要杀的话注意头文件
void ksm_migrate_page(struct page *newpage, struct page *oldpage)
{
	struct pksm_hash_node *stable_node;

	printk("PKSM : ksm_migrate_page evoked\n");

	VM_BUG_ON_PAGE(!PageLocked(oldpage), oldpage);
	VM_BUG_ON_PAGE(!PageLocked(newpage), newpage);
	VM_BUG_ON_PAGE(newpage->mapping != oldpage->mapping, newpage);

	stable_node = page_stable_node(newpage);
	if (stable_node) {
		VM_BUG_ON_PAGE(stable_node->kpfn != page_to_pfn(oldpage), oldpage);
		stable_node->kpfn = page_to_pfn(newpage);
		/*
		 * newpage->mapping was set in advance; now we need smp_wmb()
		 * to make sure that the new stable_node->kpfn is visible
		 * to get_ksm_page() before it can see that oldpage->mapping
		 * has gone stale (or that PageSwapCache has been cleared).
		 */
		smp_wmb();
		// ? 这句调用可能存在问题，可能可以和get_pksm_page()一起消除过期node
		set_page_stable_node(oldpage, NULL);
	}
}
#endif /* CONFIG_MIGRATION */

#ifdef CONFIG_MEMORY_HOTREMOVE
static void wait_while_offlining(void)
{
	printk(KERN_ALERT "PKSM : empty_function : HOTREMOVE_enabled wait_while_offlining evoked\n");
}

static void ksm_check_stable_tree(unsigned long start_pfn,
				  unsigned long end_pfn)
{
	printk(KERN_ALERT "PKSM : empty_function : HOTREMOVE_enabled ksm_check_stable_tree evoked\n");
}

static int ksm_memory_callback(struct notifier_block *self,
			       unsigned long action, void *arg)
{
	printk(KERN_ALERT "PKSM : empty_function : HOTREMOVE_enabled ksm_memory_callback evoked\n");
	return NOTIFY_OK;
}
#else
static void wait_while_offlining(void)
{
}
#endif /* CONFIG_MEMORY_HOTREMOVE */

#ifdef CONFIG_SYSFS
/*
 * This all compiles without CONFIG_SYSFS, but is a waste of space.
 */

#define PKSM_ATTR_RO(_name) \
	static struct kobj_attribute _name##_attr = __ATTR_RO(_name)
#define PKSM_ATTR(_name) \
	static struct kobj_attribute _name##_attr = \
		__ATTR(_name, 0644, _name##_show, _name##_store)

static ssize_t sleep_millisecs_show(struct kobject *kobj,
				    struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%u\n", pksm_thread_sleep_millisecs_base);
}

static ssize_t sleep_millisecs_store(struct kobject *kobj,
				     struct kobj_attribute *attr,
				     const char *buf, size_t count)
{
	unsigned long msecs;
	int err;

	err = kstrtoul(buf, 10, &msecs);
	if (err || msecs > UINT_MAX)
		return -EINVAL;

	pksm_thread_sleep_millisecs_base = msecs;

	return count;
}
PKSM_ATTR(sleep_millisecs);

static ssize_t unmerge_pages_to_scan_show(struct kobject *kobj,
				  struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%u\n", pksm_cont_unmerged_pages_threshold);
}

static ssize_t unmerge_pages_to_scan_store(struct kobject *kobj,
				   struct kobj_attribute *attr,
				   const char *buf, size_t count)
{
	int err;
	unsigned long nr_pages;

	err = kstrtoul(buf, 10, &nr_pages);
	if (err || nr_pages > UINT_MAX)
		return -EINVAL;

	pksm_cont_unmerged_pages_threshold = nr_pages;

	return count;
}
PKSM_ATTR(unmerge_pages_to_scan);

static ssize_t pages_to_scan_show(struct kobject *kobj,
				  struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%u\n", pksm_scaned_pages_threshold);
}

static ssize_t pages_to_scan_store(struct kobject *kobj,
				   struct kobj_attribute *attr,
				   const char *buf, size_t count)
{
	int err;
	unsigned long nr_pages;

	err = kstrtoul(buf, 10, &nr_pages);
	if (err || nr_pages > UINT_MAX)
		return -EINVAL;

	pksm_scaned_pages_threshold = nr_pages;

	return count;
}
PKSM_ATTR(pages_to_scan);

static ssize_t scan_step_show(struct kobject *kobj,
				  struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%u\n", pksm_cur_scan_step);
}

static ssize_t scan_step_store(struct kobject *kobj,
				   struct kobj_attribute *attr,
				   const char *buf, size_t count)
{
	int err;
	unsigned long nr_pages;

	err = kstrtoul(buf, 10, &nr_pages);
	if (err || nr_pages > UINT_MAX)
		return -EINVAL;

	pksm_cur_scan_step = nr_pages;

	return count;
}
PKSM_ATTR(scan_step);

static ssize_t run_show(struct kobject *kobj, struct kobj_attribute *attr,
			char *buf)
{
	return sprintf(buf, "%lu\n", pksm_run);
}

static ssize_t run_store(struct kobject *kobj, struct kobj_attribute *attr,
			 const char *buf, size_t count)
{
	int err;
	unsigned long flags;

	err = kstrtoul(buf, 10, &flags);
	if (err || flags > UINT_MAX)
		return -EINVAL;
	if (flags > PKSM_RUN_UNMERGE)
		return -EINVAL;

	// printk("PKSM : run_store evoked with flags = %lu\n", flags);

	/*
	 * PKSM_RUN_MERGE sets ksmd running, and 0 stops it running.
	 * PKSM_RUN_UNMERGE stops it running and unmerges all rmap_items,
	 * breaking COW to free the pages_shared (but leaves mm_slots
	 * on the list for when ksmd may be set running again).
	 */

	mutex_lock(&pksm_thread_mutex);
	wait_while_offlining();
	if (pksm_run != flags) {
		pksm_run = flags;
		printk(KERN_ALERT "PKSM : run_store : now pksm_run = %lu\n", pksm_run);

		#ifdef USE_ADVANCED_MEMCMP
		printk(KERN_ALERT "PKSM : USE_ADVANCED_MEMCMP defined\n");
		#endif

		#ifdef SYST_NOINLINE
		printk(KERN_ALERT "PKSM : SYST_NOINLINE defined\n");
		#endif

		if (flags & PKSM_RUN_UNMERGE) {
			// printk("PKSM : run_store PKSM_RUN_UNMERGE\n");
			// set_current_oom_origin();
			// err = unmerge_and_remove_all_rmap_items();
			// clear_current_oom_origin();
			// if (err) {
			// 	pksm_run = PKSM_RUN_STOP;
			// 	count = err;
			// }
		}
	}
	mutex_unlock(&pksm_thread_mutex);

	if (flags & PKSM_RUN_MERGE)
		wake_up_interruptible(&pksm_thread_wait);

	return count;
}
PKSM_ATTR(run);

#ifdef CONFIG_NUMA
static ssize_t merge_across_nodes_show(struct kobject *kobj,
				struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%u\n", ksm_merge_across_nodes);
}

static ssize_t merge_across_nodes_store(struct kobject *kobj,
				   struct kobj_attribute *attr,
				   const char *buf, size_t count)
{
	int err;
	unsigned long knob;

	err = kstrtoul(buf, 10, &knob);
	if (err)
		return err;
	if (knob > 1)
		return -EINVAL;

	mutex_lock(&pksm_thread_mutex);
	wait_while_offlining();
	if (ksm_merge_across_nodes != knob) {
		if (pksm_pages_shared || remove_all_stable_nodes())
			err = -EBUSY;
		else if (root_stable_tree == one_stable_tree) {
			struct rb_root *buf;
			/*
			 * This is the first time that we switch away from the
			 * default of merging across nodes: must now allocate
			 * a buffer to hold as many roots as may be needed.
			 * Allocate stable and unstable together:
			 * MAXSMP NODES_SHIFT 10 will use 16kB.
			 */
			buf = kcalloc(nr_node_ids + nr_node_ids, sizeof(*buf),
				      GFP_KERNEL);
			/* Let us assume that RB_ROOT is NULL is zero */
			if (!buf)
				err = -ENOMEM;
			else {
				root_stable_tree = buf;
				root_unstable_tree = buf + nr_node_ids;
				/* Stable tree is empty but not the unstable */
				root_unstable_tree[0] = one_unstable_tree[0];
			}
		}
		if (!err) {
			ksm_merge_across_nodes = knob;
			ksm_nr_node_ids = knob ? 1 : nr_node_ids;
		}
	}
	mutex_unlock(&pksm_thread_mutex);

	return err ? err : count;
}
PKSM_ATTR(merge_across_nodes);
#endif

static ssize_t pksm_meta_show(struct kobject *kobj,
				 struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "rmap_item\n%lu\nhash_node\n%lu\npage_slot\n%lu\n", pksm_rmap_items, pksm_node_items, pksm_pages_inlist);
}
PKSM_ATTR_RO(pksm_meta);

static ssize_t pages_shared_show(struct kobject *kobj,
				 struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%lu\n", pksm_pages_shared);
}
PKSM_ATTR_RO(pages_shared);

static ssize_t pages_sharing_show(struct kobject *kobj,
				  struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%lu\n", pksm_pages_sharing);
}
PKSM_ATTR_RO(pages_sharing);

static ssize_t pages_unshared_show(struct kobject *kobj,
				   struct kobj_attribute *attr, char *buf)
{
	long pksm_pages_unshared;
	pksm_pages_unshared = pksm_node_items-pksm_pages_shared;
	return sprintf(buf, "%lu\n", pksm_pages_unshared);
}
PKSM_ATTR_RO(pages_unshared);

static ssize_t pages_inlist_show(struct kobject *kobj,
				   struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%lu\n", pksm_pages_inlist);
}
PKSM_ATTR_RO(pages_inlist);

// static ssize_t pages_volatile_show(struct kobject *kobj,
// 				   struct kobj_attribute *attr, char *buf)
// {
// 	long pksm_pages_volatile;

// 	pksm_pages_volatile = ksm_rmap_items - pksm_pages_shared
// 				- pksm_pages_sharing - pksm_pages_unshared;
// 	/*
// 	 * It was not worth any locking to calculate that statistic,
// 	 * but it might therefore sometimes be negative: conceal that.
// 	 */
// 	if (ksm_pages_volatile < 0)
// 		ksm_pages_volatile = 0;
// 	return sprintf(buf, "%ld\n", ksm_pages_volatile);
// }
// PKSM_ATTR_RO(pages_volatile);

static ssize_t full_scans_show(struct kobject *kobj,
			       struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%lu\n", pksm_scan.seqnr);
}
PKSM_ATTR_RO(full_scans);

static ssize_t pages_merged_show(struct kobject *kobj,
			       struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%lu\n", pksm_pages_merged);
}
PKSM_ATTR_RO(pages_merged);

static ssize_t sleep_real_show(struct kobject *kobj,
			       struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%u\n", pksm_thread_sleep_millisecs_real);
}
PKSM_ATTR_RO(sleep_real);

static ssize_t last_merged_show(struct kobject *kobj,
			       struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%u\n", pksm_last_merged_pages);
}
PKSM_ATTR_RO(last_merged);

static ssize_t last_unmerged_show(struct kobject *kobj,
			       struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%u\n", pksm_last_unmerged_pages);
}
PKSM_ATTR_RO(last_unmerged);

static ssize_t zero_merged_show(struct kobject *kobj,
			       struct kobj_attribute *attr, char *buf)
{
	return sprintf(buf, "%lu\n", pksm_zero_merged);
}
PKSM_ATTR_RO(zero_merged);

static ssize_t scan_step_cnt_show(struct kobject *kobj,
			       struct kobj_attribute *attr, char *buf)
{
	int i, size;
	char *p = buf;

	for (i = 0; i < 5; i++) {
		size = sprintf(p, "%u ", pksm_scan_step_cnts[i]);
		p += size;
	}

	*p++ = '\n';
	*p = '\0';

	return p - buf;
}
PKSM_ATTR_RO(scan_step_cnt);

static ssize_t scan_step_pervage_cnt_show(struct kobject *kobj,
			       struct kobj_attribute *attr, char *buf)
{
	int i, size;
	char *p = buf;

	for (i = 0; i < 6; i++) {
		size = sprintf(p, "%u ", pksm_scan_step_pervage_cnts[i]);
		p += size;
	}

	*p++ = '\n';
	*p = '\0';

	return p - buf;
}
PKSM_ATTR_RO(scan_step_pervage_cnt);

static struct attribute *pksm_attrs[] = {
	&pksm_meta_attr.attr,
	&zero_merged_attr.attr,
	&scan_step_attr.attr,
	&unmerge_pages_to_scan_attr.attr,
	&last_unmerged_attr.attr,
	&last_merged_attr.attr,
	&sleep_real_attr.attr,
	&sleep_millisecs_attr.attr,
	&pages_to_scan_attr.attr,
	&run_attr.attr,
	&pages_shared_attr.attr,
	&pages_sharing_attr.attr,
	&pages_unshared_attr.attr,
	&pages_merged_attr.attr,
	&pages_inlist_attr.attr,
	// &pages_volatile_attr.attr,
	&full_scans_attr.attr,
	&scan_step_cnt_attr.attr,
	&scan_step_pervage_cnt_attr.attr,
#ifdef CONFIG_NUMA
	&merge_across_nodes_attr.attr,
#endif
	NULL,
};

static struct attribute_group pksm_attr_group = {
	.attrs = pksm_attrs,
	.name = "pksm",
};
#endif /* CONFIG_SYSFS */

static int __init pksm_init(void)
{
	struct task_struct *pksm_thread;
	int err;
	uint32_t partial_hash;

	printk(KERN_ALERT "PKSM : page_list_lock%p\n", &pksm_pagelist_lock);

	zero_hash = calc_hash(ZERO_PAGE(0), &partial_hash);

	err = pksm_slab_init();
	if (err)
		goto out;

	pksm_thread = kthread_run(pksm_scan_thread, NULL, "pksmd");

	if (IS_ERR(pksm_thread)) {
		pr_err("PKSM : creating kthread failed\n");
		err = PTR_ERR(pksm_thread);
		goto out_free;
	}

#ifdef CONFIG_SYSFS
	err = sysfs_create_group(mm_kobj, &pksm_attr_group);
	if (err) {
		pr_err("PKSM : register sysfs failed\n");
		kthread_stop(pksm_thread);
		goto out_free;
	}
#else
	pksm_run = PKSM_RUN_MERGE;	/* no way for user to start it */

#endif /* CONFIG_SYSFS */

#ifdef CONFIG_MEMORY_HOTREMOVE
	/* There is no significance to this priority 100 */
	printf("PKSM : CONFIG_MEMORY_HOTREMOVE defined\n");

	// hotplug_memory_notifier(pksm_memory_callback, 100);
#endif
	return 0;

out_free:
	pksm_slab_free();
out:
	return err;
}

subsys_initcall(pksm_init);
