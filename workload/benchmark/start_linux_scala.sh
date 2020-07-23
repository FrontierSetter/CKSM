my_log="./" 
> ${my_log}"timestamp_linux_scala.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_linux_scala.log"

    ./linux-scalability 512 1000000 8
    sleep 2
done

"end" >> ${my_log}"timestamp_elastic.log"
date +%s >> ${my_log}"timestamp_elastic.log"
