my_log="./" 
name="memtest"
> ${my_log}"timestamp_memtest.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_memtest.log"

    memtester 4G 2 &
    sleep 1
    # docker run -d kibana:7.5.1
    # sleep 6
done

date +%s >> ${my_log}"timestamp_memtest.log"
