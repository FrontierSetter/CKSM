name="spark"
echo "" > ${my_log}"timestamp_spark.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_spark.log"

    docker run --name "spark-master-$i" -h "spark-master-$i" -e ENABLE_INIT_DAEMON=false -d bde2020/spark-master:2.4.4-hadoop2.7
    sleep 1

    docker run --name "spark-worker-1-$i" --link "spark-master-$i":spark-master -e ENABLE_INIT_DAEMON=false -d bde2020/spark-worker:2.4.4-hadoop2.7
    sleep 1

    docker run --name "spark-worker-2-$i" --link "spark-master-$i":spark-master -e ENABLE_INIT_DAEMON=false -d bde2020/spark-worker:2.4.4-hadoop2.7
    sleep 1

    docker run --name "spark-worker-3-$i" --link "spark-master-$i":spark-master -e ENABLE_INIT_DAEMON=false -d bde2020/spark-worker:2.4.4-hadoop2.7
    sleep 1

    
done