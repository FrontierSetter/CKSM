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

struct pksm_hash_node{
	unsigned long kpfn;
    struct hlist_node hlist;
	page_slot *page_slot;	//反向映射到对应的slot
							//是为了在unstable table中找到后可以在merge时从table中移除
};

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

// TODO
PagePksm()
pksm_test_exit(page_slot*)
free_stable_node()

// 和ksm_page()一样直接删除stable_node
get_pksm_page(pksm_hash_node*, bool)

分配一个pksm_hash_node

哈希表中删除用hash_del 还是另一个

break_cow(??)

int rmap_walk_ksm(struct page *page, struct rmap_walk_control *rwc)

// ! 注意

hlist_for_each_entry() 的参数不一样

ksm建立的重映射是否要加入反向映射队列？