my_zero_pfn(addr)	
    |
    |
page_to_pfn(ZERO_PAGE(addr))
                |
                |
page_to_pfn(phys_to_page(__pa_symbol(empty_zero_page)))
                |
                |
page_to_pfn((pfn_to_page(__phys_to_pfn(__pa_symbol(empty_zero_page)))))
                                            |
                                            |
page_to_pfn((pfn_to_page(__phys_to_pfn(__phys_addr_symbol(RELOC_HIDE((unsigned long)(empty_zero_page), 0))))))
                                                                |
                                                                |
page_to_pfn((pfn_to_page(__phys_to_pfn(__phys_addr_symbol((unsigned long)(empty_zero_page))))))
                                            |
                                            |
page_to_pfn((pfn_to_page(__phys_to_pfn(__pa_symbol_nodebug((unsigned long)(empty_zero_page))))))
                                            |
                                            |
page_to_pfn((pfn_to_page(__phys_to_pfn(__kimg_to_phys((phys_addr_t)(empty_zero_page))))))
                                            |
                                            |
page_to_pfn((pfn_to_page(__phys_to_pfn((phys_addr_t)(empty_zero_page) - kimage_voffset))))
                            |
                            |
page_to_pfn((pfn_to_page(PHYS_PFN((phys_addr_t)(empty_zero_page) - kimage_voffset))))
                            |
                            |
page_to_pfn((pfn_to_page((unsigned long)((x) >> PAGE_SHIFT)))) ; x = ((phys_addr_t)(empty_zero_page) - kimage_voffset)



page_to_pfn：从page到pfn号
pfn_to_page：从pfn到page
__phys_to_pfn：从物理地址到pfn，直接移位
__pa_symbol->__pa_symbol_nodebug->__pa_symbol_nodebug->__kimg_to_phys：从内核镜像到物理地址，减去一个偏移
