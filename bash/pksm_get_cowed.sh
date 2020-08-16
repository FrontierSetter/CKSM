my_log="./test_data/" 

> ${my_log}"page_cowed.log"

while true;
do
	/bin/sleep 1

	date +%s >> ${my_log}"page_cowed.log"
	echo 'page_cowed' >> ${my_log}"page_cowed.log"
    cat /sys/kernel/mm/pksm/pages_cowed >> ${my_log}"page_cowed.log"
done