if(($# > 0))
then
    echo "everything"
    cp ./pgtable.h /home/l/kernel-src/pksm-5.7/include/asm-generic/pgtable.h
    cp ./fork.c /home/l/kernel-src/pksm-5.7/kernel/fork.c
    cp ./memory.c /home/l/kernel-src/pksm-5.7/mm/memory.c
    cp ./page_alloc.c /home/l/kernel-src/pksm-5.7/mm/page_alloc.c
    cp ./pksm.h /home/l/kernel-src/pksm-5.7/include/linux/ksm.h
    # cp ./config ~/kernel-src/pksm-4.2.9/.config
fi

cp ./pksm.c /home/l/kernel-src/pksm-5.7/mm/ksm.c




