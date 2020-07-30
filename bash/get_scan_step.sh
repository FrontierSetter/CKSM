my_log="./test_data/" 

> ${my_log}"scan_step_cnt.log"

while true;
do
	/bin/sleep 1

	date +%s >> ${my_log}"scan_step_cnt.log"
	cat /sys/kernel/mm/pksm/scan_step_cnt >> ${my_log}"scan_step_cnt.log"

	cat /sys/kernel/mm/pksm/scan_step_pervage_cnt >> ${my_log}"scan_step_cnt.log"
done