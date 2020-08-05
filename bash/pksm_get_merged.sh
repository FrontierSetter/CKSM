my_log="./test_data/" 

> ${my_log}"pksm_merged.log"

while true;
do
	/bin/sleep 1

	date +%s >> ${my_log}"pksm_merged.log"
	echo 'page_merged' >> ${my_log}"pksm_merged.log"
    cat /sys/kernel/mm/pksm/pages_merged >> ${my_log}"pksm_merged.log"
    echo 'page_zero_merged' >> ${my_log}"pksm_merged.log"
    cat /sys/kernel/mm/pksm/zero_merged >> ${my_log}"pksm_merged.log"
done