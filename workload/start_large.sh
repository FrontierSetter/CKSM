my_log="./" 
name="large"
> ${my_log}"timestamp_large.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_large.log"

    ./start_nginx_batch.sh 32
    sleep 1
    ./start_elastic.sh 10
    sleep 1
    # docker run -d kibana:7.5.1
    # sleep 6
done

date +%s >> ${my_log}"timestamp_large.log"