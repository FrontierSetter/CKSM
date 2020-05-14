name="redis"

for ((i=0;i<$1;i++))
do
    echo "$name$i"
	# date +%s >> ${my_log}"timestamp_redis.log"

    docker run -d redis

    sleep 1
done