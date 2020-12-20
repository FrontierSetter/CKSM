name="stitch"
echo "" > ${my_log}"timestamp_stitch.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_stitch.log"

    # docker run -d -e "discovery.type=single-node" elasticsearch:7.5.1
    # sleep 2

    docker run -d mongo


    # docker run -d rabbitmq
    # sleep 1

    docker run -d couchbase
    sleep 3
    # docker run -d kibana:7.5.1
    # sleep 6
    
done