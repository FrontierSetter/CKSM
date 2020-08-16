my_log="./test_data/" 

> ${my_log}"ksm_merged.log"

while true;
do
	/bin/sleep 1

	date +%s >> ${my_log}"ksm_merged.log"
	echo 'page_merged' >> ${my_log}"ksm_merged.log"
    cat /sys/kernel/mm/ksm/pages_merged >> ${my_log}"ksm_merged.log"
done