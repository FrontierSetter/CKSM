# docker stop $(docker ps -aq)
# docker rm $(docker ps -aq)

name="php"
echo "" > ${my_log}"timestamp_php.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_php.log"

    docker run -d php

    sleep 1
done