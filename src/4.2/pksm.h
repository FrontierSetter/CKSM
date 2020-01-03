#ifndef __LINUX_KSM_H
#define __LINUX_KSM_H
/*
 * Memory merging support.
 *
 * This code enables dynamic sharing of identical pages found in different
 * memory areas, even if they are not shared by fork().
 */

#include <linux/bitops.h>
#include <linux/mm.h>
#include <linux/pagemap.h>
#include <linux/rmap.h>
#include <linux/sched.h>

struct stable_node;
struct mem_cgroup;

#ifdef CONFIG_KSM
int ksm_madvise(struct vm_area_struct *vma, unsigned long start,
		unsigned long end, int advice, unsigned long *vm_flags);
// int __ksm_enter(struct mm_struct *mm);
void __pksm_exit(struct page *page);
void pksm_new_anon_page(struct page *page, bool high_priority);

static inline int ksm_fork(struct mm_struct *mm, struct mm_struct *oldmm)
{
	// if (test_bit(MMF_VM_MERGEABLE, &oldmm->flags))
	// 	return __ksm_enter(mm);
	return 0;
}

static inline void pksm_exit(struct page *page)
{
	__pksm_exit(page);
}

/*
 * A KSM page is one of those write-protected "shared pages" or "merged pages"
 * which KSM maps into multiple mms, wherever identical anonymous page content
 * is found in VM_MERGEABLE vmas.  It's a PageAnon page, pointing not to any
 * anon_vma, but to that page's node of the stable tree.
 */

// 这里改个名是为了模块内部命名的一致性，但是发现PageKsm在外部也被调用（毕竟是在.h文件里）
// 4.2里吧PageKsm移到了page-flags.h里
// 所以两个都保留（很蠢，但是懒得改）
// ? 这个东西会在rmap_walk作为函数对象使用，是不是不能inline？
static int PagePksm(struct page *page)
{
	return ((unsigned long)page->mapping & PAGE_MAPPING_FLAGS) ==
				(PAGE_MAPPING_ANON | PAGE_MAPPING_KSM);
}

static inline int PagePksm_inline(struct page *page)
{
	return ((unsigned long)page->mapping & PAGE_MAPPING_FLAGS) ==
				(PAGE_MAPPING_ANON | PAGE_MAPPING_KSM);
}

static inline struct pksm_hash_node *page_stable_node(struct page *page)
{
	return PagePksm(page) ? page_rmapping(page) : NULL;
}

static inline void set_page_stable_node(struct page *page,
					struct pksm_hash_node *pksm_hash_node)
{
	page->mapping = (void *)pksm_hash_node +
				(PAGE_MAPPING_ANON | PAGE_MAPPING_KSM);
}

/*
 * When do_swap_page() first faults in from swap what used to be a KSM page,
 * no problem, it will be assigned to this vma's anon_vma; but thereafter,
 * it might be faulted into a different anon_vma (or perhaps to a different
 * offset in the same anon_vma).  do_swap_page() cannot do all the locking
 * needed to reconstitute a cross-anon_vma KSM page: for now it has to make
 * a copy, and leave remerging the pages to a later pass of ksmd.
 *
 * We'd like to make this conditional on vma->vm_flags & VM_MERGEABLE,
 * but what if the vma was unmerged while the page was swapped out?
 */
struct page *ksm_might_need_to_copy(struct page *page,
			struct vm_area_struct *vma, unsigned long address);

int rmap_walk_ksm(struct page *page, struct rmap_walk_control *rwc);
void ksm_migrate_page(struct page *newpage, struct page *oldpage);

#else  /* !CONFIG_KSM */

static inline int ksm_fork(struct mm_struct *mm, struct mm_struct *oldmm)
{
	return 0;
}

static inline void ksm_exit(struct mm_struct *mm)
{
}


#ifdef CONFIG_MMU
static inline int ksm_madvise(struct vm_area_struct *vma, unsigned long start,
		unsigned long end, int advice, unsigned long *vm_flags)
{
	return 0;
}

static inline struct page *ksm_might_need_to_copy(struct page *page,
			struct vm_area_struct *vma, unsigned long address)
{
	return page;
}

static inline int page_referenced_ksm(struct page *page,
			struct mem_cgroup *memcg, unsigned long *vm_flags)
{
	return 0;
}

static inline int rmap_walk_ksm(struct page *page,
			struct rmap_walk_control *rwc)
{
	return 0;
}

static inline void ksm_migrate_page(struct page *newpage, struct page *oldpage)
{
}
#endif /* CONFIG_MMU */
#endif /* !CONFIG_KSM */

#endif /* __LINUX_KSM_H */
