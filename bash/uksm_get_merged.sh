my_log="./test_data/" 

> ${my_log}"uksm_merged.log"

while true;
do
	/bin/sleep 1

	date +%s >> ${my_log}"uksm_merged.log"
	echo 'page_merged' >> ${my_log}"uksm_merged.log"
    cat /sys/kernel/mm/uksm/pages_merged >> ${my_log}"uksm_merged.log"
    echo 'page_zero_merged' >> ${my_log}"uksm_merged.log"
    cat /sys/kernel/mm/uksm/pages_zero_merged >> ${my_log}"uksm_merged.log"
done