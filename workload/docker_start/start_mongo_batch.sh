name="mongo"
echo "" > ${my_log}"timestamp_mongo.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_mongo.log"

    docker run -d bitnami/mongodb:latest

    sleep 1
done