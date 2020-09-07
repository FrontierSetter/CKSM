my_log="./test_data/" 

> ${my_log}"meta_usage.log"

while true;
do
	/bin/sleep 1

	date +%s >> ${my_log}"meta_usage.log"
    cat /sys/kernel/mm/ksm/ksm_meta >> ${my_log}"meta_usage.log"
done