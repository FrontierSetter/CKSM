for ((i=0;i<$1;i++))
do
    echo "sysbench_$i"

    sysbench --test=memory --num-threads=4 --memory-block-size=4K --memory-total-size=100G --memory-access-mode=seq --memory-oper=read run > "mem_read_seq_$i"
    sysbench --test=memory --num-threads=4 --memory-block-size=4K --memory-total-size=100G --memory-access-mode=seq --memory-oper=write run > "mem_write_seq_$i"

    sysbench --test=memory --num-threads=4 --memory-block-size=4K --memory-total-size=100G --memory-access-mode=rnd --memory-oper=read run > "mem_read_rnd_$i"
    sysbench --test=memory --num-threads=4 --memory-block-size=4K --memory-total-size=100G --memory-access-mode=rnd --memory-oper=write run > "mem_write_rnd_$i"

    # sysbench --test=cpu --cpu-max-prime=20000 run > "cpu_$i"

    # sysbench --test=fileio --file-total-size=2G prepare
    # sysbench --test=fileio --file-total-size=2G --file-block-size=4096 --file-io-mode=mmap --file-test-mode=rndrw --file-extra-flags=direct run > "file_rw_rnd_$i"
    # sysbench --test=fileio --file-total-size=2G cleanup

    # sysbench --test=fileio --file-total-size=2G prepare
    # sysbench --test=fileio --file-total-size=2G --file-block-size=4096 --file-io-mode=mmap --file-test-mode=seqrewr  --file-extra-flags=direct run > "file_rw_seq_$i"
    # sysbench --test=fileio --file-total-size=2G cleanup

done