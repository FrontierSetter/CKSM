// page在扫描链中的封装结构
struct page_slot {
	struct list_head page_list;
	struct page *physical_page;
	struct pksm_hash_node *page_item;
    bool invalid;	// page被merge到一个pksmpage之后会被置为true
}

// 下一个要被扫描的slot
struct pksm_scan{
	struct page_slot *page_slot;
	unsigned long seqnr;
};

// page_slot链表的头部
static struct page_slot pksm_page_head = {
	.page_list = LIST_HEAD_INIT(pksm_page_head.page_list)
}

// 用于修改pksm_scan->page_slot的锁
static DEFINE_SPINLOCK(pksm_pagelist_lock);

// 获取下一个page
static struct page_slot *scan_get_next_page_slot()

static void pksm_cmp_and_merge_page(struct page_slot *cur_page_slot)



struct pksm_hash_node{
	unsigned long kpfn;
    struct hlist_node hlist;
	page_slot *page_slot;	//反向映射到对应的slot
							//是为了在unstable table中找到后可以在merge时从table中移除
	struct hlist_head rmap_list;
};

struct pksm_rmap_item{
	struct hlist_node hlist;
	struct anon_vma *anon_vma;
	struct mm_struct *mm;
	unsigned long address;
}

struct rmap_process_wrapper{
	struct pksm_hash_node *pksm_hash_node;
	struct page *kpage; 
}

#define PAGE_HASH_BIT 18 // 256K
#define PAGE_HASH_MASK 262143
static DEFINE_HASHTABLE(stable_hash_table, PAGE_HASH_BIT);
static DEFINE_HASHTABLE(unstable_hash_table, PAGE_HASH_BIT);

static struct page *unstable_hash_search_insert(struct page *page, unsigned int entryIndex)
static struct page *stable_hash_search(struct page *page, unsigned int entryIndex)

static void remove_node_from_hashlist(struct page_slot *page_slot)

static int try_to_merge_with_pksm_page(struct page_slot *page_slot, 
					  struct page *page, struct page *kpage)
要不要加锁

static int pksm_try_to_merge_one_page(struct page *page, struct page *kpage)

// 修改形参列表
try_to_merge_one_page(struct page *page, struct vm_area_struct *vma,
		     unsigned long address, void *arg)

static struct page * pksm_try_to_merge_two_pages(struct page_slot *page_slot, struct page *page, 
							struct *table_page_slot, struct page *table_page)

static struct pksm_hash_node *stable_hash_insert(struct page_slot *kpage_slot, struct page *kpage){

PagePksm()

pksm_test_exit(page_slot*)	//? 暂时用的_mapcount，或许可以用_count，见mm.h/get_page_unless_zero

get_pksm_page(pksm_hash_node*, bool)

static struct kmem_cache *pksm_hash_node_cache;
static struct kmem_cache *page_slot_cache;

static int __init pksm_slab_init(void)
static void __init pksm_slab_free(void)


static inline struct stable_node *alloc_hash_node(void)

static inline void free_hash_node(struct pksm_hash_node *pksm_hash_node)

static inline struct page_slot *alloc_page_slot(void)

static inline void free_page_slot(struct page_slot *page_slot)

static inline struct pksm_rmap_item *alloc_pksm_rmap_item(void)

static inline void free_pksm_rmap_item(struct pksm_rmap_item *pksm_rmap_item)

int rmap_walk_ksm(struct page *page, struct rmap_walk_control *rwc)

pksm_run及其相关宏{
	#define PKSM_RUN_STOP	0
	#define PKSM_RUN_MERGE	1
	#define PKSM_RUN_UNMERGE	2
	#define PKSM_RUN_OFFLINE	4

	static unsigned long pksm_run = PKSM_RUN_STOP;
}

pksm_scan_thread

pksmd_should_run()

pksm_do_scan

wait_while_offlining(); // 不用改（应该）

pksm_thread_mutex

pksm_thread_wait	//这是个等待队列头


// TODO
哈希表中删除用hash_del 还是另一个 -> 区别不大

break_cow(??)

hotplug_memory_notifier(pksm_memory_callback, 100);

暂时没有区分stable_node和普通的hash_node 

int ksm_madvise(struct vm_area_struct *vma, unsigned long start,

__ksm_enter

static int ksm_memory_callback(struct notifier_block *self,
			       unsigned long action, void *arg)

static void ksm_check_stable_tree(unsigned long start_pfn,
				  unsigned long end_pfn)


// ! 注意

hlist_for_each_entry() 的参数不一样

ksm建立的重映射是否要加入反向映射队列？

// printk()要不要include头文件



// ? 关于pksm之后反向映射机制的兼容性
在merge_with_pksm_page()的层次看不到vma
在merge操作的层次都看不到hash_node

ksm中rmap_item作为操作对象（虚拟页）的代表穿插在操作的每个阶段中，穿针引线
在merge阶段获得对应的anon_vma，在stable_node插入阶段挂载上对应的节点

但是在pksm中没有rmap_item这一单元，直接的操作对象就是page（page_slot）
通过page_slot来穿针引线
page_slot->page_item获得hash_node，在merge阶段可以看到vma，直接创造rmap_item挂上对应的hash_node


ksm中 
	1、rmap_item的创建
	2、anon_vma对象的指派
	3、rmap_item向node的挂载
之分离的

pksm中全部集中在try_merge_one_page()中

这就需要在进入merge_one_page()之前page_slot就已经有了一个合法的hash_node

如果是和一个pksm页面合并，则它必然有一个hash_node，只要把新页面的每个vma都封装成rmap_item然后挂载上去就行
如果是把一个页面升级成pksm页面，则分配一个hash_node，再通过anon_walk遍历它的vma作为rmap_item挂载上去


// ? 关于ksm中的参数设置与输出
暂时不知道改名会不会对文件绑定产生影响，因此不改名
pksm_attr_group 利用 struct attribute 结构进行控制属性向用户的开放与绑定
https://blog.csdn.net/qq_16777851/article/details/81396047
// 但是一开始的xxx_attr.attr变量不知道怎么产生
通过 KSM_ATTR_RO宏产生只读的属性绑定
