name="elastic"
echo "" > ${my_log}"timestamp_elastic.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_elastic.log"

    docker run -d -e "discovery.type=single-node" elasticsearch:7.5.1
    sleep 3
    # docker run -d kibana:7.5.1
    # sleep 6
    
done