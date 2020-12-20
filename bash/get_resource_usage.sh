my_log="./test_data/" 
pksm_thread=`ps -ef | grep -v grep | grep $1 | awk '{print $2}'`

> ${my_log}"cpu_usage.log"
> ${my_log}"mem_usage.log"

while true;
do
	/bin/sleep 1

	date +%s >> ${my_log}"cpu_usage.log"
	top -b -p $pksm_thread -n 1 -d 1| grep $1 >> ${my_log}"cpu_usage.log"

	date +%s >> ${my_log}"mem_usage.log"
	free -b >> ${my_log}"mem_usage.log"
done