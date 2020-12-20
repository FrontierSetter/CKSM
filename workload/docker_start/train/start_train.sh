name="train"
echo "" > ${my_log}"timestamp_train.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_train.log"

    docker run -d anibali/pytorch:no-cuda python
    docker run -d memcached
    docker run -d tensorflow/tensorflow
    docker run -d memcached

    sleep 1
done
