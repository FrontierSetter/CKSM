my_log="./test_data/" 

echo "" > ${my_log}"cpu_usage.log"
echo "" > ${my_log}"mem_usage.log"

while true;
do
	/bin/sleep 1

	date +%s >> ${my_log}"cpu_usage.log"
	top -b -p $1 -n 1 -d 1| grep $2 >> ${my_log}"cpu_usage.log"

	date +%s >> ${my_log}"mem_usage.log"
	free -b >> ${my_log}"mem_usage.log"
done