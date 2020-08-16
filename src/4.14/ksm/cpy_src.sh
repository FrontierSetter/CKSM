if(($# > 0))
then
    echo "everything"
    cp ./fork.c /home/l/kernel-src/linux-4.14/kernel/fork.c
    cp ./mmap.c /home/l/kernel-src/linux-4.14/mm/mmap.c
    cp ./ksm.h /home/l/kernel-src/linux-4.14/include/linux/ksm.h
    # cp ./config ~/kernel-src/pksm-4.2.9/.config
fi

cp ./ksm.c /home/l/kernel-src/linux-4.14/mm/ksm.c




