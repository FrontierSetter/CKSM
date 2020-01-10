# ./start_mysql_batch.sh $1 &
# ./start_lamp_batch.sh $1 &
# ./start_httpd_batch.sh $1 &

name="lamp"
echo "" > ${my_log}"timestamp_lamp.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_lamp.log"

    docker run -d php
    # docker run -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql
    docker run -e POSTGRES_PASSWORD="mysecretpassword$i" -d postgres
    docker run -d httpd


    sleep 1
done