my_log="./test_data/" 

echo > ${my_log}"mem_usage.log"

while true;
do
	/bin/sleep 1

	date +%s >> ${my_log}"mem_usage.log"
	free -b >> ${my_log}"mem_usage.log"
done