# docker stop $(docker ps -aq)
# docker rm $(docker ps -aq)

name="httpd"
echo "" > ${my_log}"timestamp_httpd.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_httpd.log"

    docker run -d httpd

    sleep 1
done