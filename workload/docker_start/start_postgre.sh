name="postgres"
echo "" > ${my_log}"timestamp_postgres.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_postgres.log"

    docker run -e POSTGRES_PASSWORD="mysecretpassword$i" -d postgres

    sleep 1
done