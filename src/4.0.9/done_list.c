// page在扫描链中的封装结构
struct page_slot {
	struct list_head page_list;
	struct page *physical_page;
	struct pksm_hash_node *page_item;
    bool invalid;
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
};

#define PAGE_HASH_BIT 18 // 256K
#define PAGE_HASH_MASK 262143
static DEFINE_HASHTABLE(stable_hash_table, PAGE_HASH_BIT);
static DEFINE_HASHTABLE(unstable_hash_table, PAGE_HASH_BIT);

static struct page *unstable_hash_search_insert(struct page *page, unsigned int entryIndex)
static struct page *stable_hash_search(struct page *page, unsigned int entryIndex)


// TODO
PagePksm()
pksm_test_exit(page_slot*)
free_stable_node()

// 和ksm_page()一样直接删除stable_node
get_pksm_page(pksm_hash_node*, bool)

// 把page_item从树中移除
remove_node_from_tree(hlist_node *)

// 直接归并两个物理页，需要利用反向映射机制
try_to_merge_with_ksm_page(struct page *page, struct page *kpage)

try_to_merge_two_pages(struct page *page, struct page *kpage)

stable_tree_insert(struct page *page)

unstable_hash_search_insert()中的一部分,分配一个pksm_hash_node

哈希表中删除用hash_del 还是另一个

break_cow(??)


// ! 注意

hlist_for_each_entry() 的参数不一样

ksm建立的重映射是否要加入反向映射队列？