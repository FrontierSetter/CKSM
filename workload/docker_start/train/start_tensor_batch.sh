# docker stop $(docker ps -aq)
# docker rm $(docker ps -aq)

name="tensor"
echo "" > ${my_log}"timestamp_tensor.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_tensor.log"

    docker run -d tensorflow/tensorflow

    sleep 1
done