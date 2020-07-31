# docker stop $(docker ps -aq)
# docker rm $(docker ps -aq)

name="couchbase"
echo "" > ${my_log}"timestamp_couchbase.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_couchbase.log"

    docker run -d couchbase

    sleep 1
done