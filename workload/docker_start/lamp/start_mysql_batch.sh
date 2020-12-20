# docker stop $(docker ps -aq)
# docker rm $(docker ps -aq)

name="mysql"
echo "" > ${my_log}"timestamp_mysql.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_mysql.log"

    docker run -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql

    sleep 1
done