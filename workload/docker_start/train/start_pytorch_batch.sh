# docker stop $(docker ps -aq)
# docker rm $(docker ps -aq)

name="pytorch"
echo "" > ${my_log}"timestamp_pytorch.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_pytorch.log"

    docker run -d anibali/pytorch:no-cuda

    sleep 1
done