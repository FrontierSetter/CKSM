# docker stop $(docker ps -aq)
# docker rm $(docker ps -aq)

name="tomcat"
echo "" > ${my_log}"timestamp_tormcat.log"

for ((i=0;i<$1;i++))
do
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_tormcat.log"

    docker run -it --rm tomcat
    sleep 1
done