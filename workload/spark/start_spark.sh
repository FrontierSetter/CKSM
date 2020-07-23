my_log="./" 
name="spark"
> ${my_log}"timestamp_spark.log"

for ((i=0;i<$1;i++))
do
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_spark.log"

    docker run -e ENABLE_INIT_DAEMON=false --link spark-master:spark-master --net eurospark_default -v /home/l/workload/spark/euro_spark/txt/input.txt:/app/input.txt -d bde/spark-app
    sleep 2

done

echo "end" >> ${my_log}"timestamp_spark.log"
date +%s >> ${my_log}"timestamp_spark.log"
