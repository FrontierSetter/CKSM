ori_log="/sys/kernel/mm/ksm/"
my_log="./test_data/" 

echo "" > ${my_log}"ksm_pages_sharing.log"
echo "" > ${my_log}"ksm_pages_shared.log"
echo "" > ${my_log}"ksm_pages_merged.log"

# echo "" > ${my_log}"cpu_consumption.log"


while true;
do
	sleep 0.1

	date +%s >> ${my_log}"ksm_pages_sharing.log"
	cat ${ori_log}"pages_sharing" >> ${my_log}"ksm_pages_sharing.log"
	date +%s >> ${my_log}"ksm_pages_shared.log"
	cat ${ori_log}"pages_shared" >> ${my_log}"ksm_pages_shared.log"
	date +%s >> ${my_log}"ksm_pages_merged.log"
	cat ${ori_log}"pages_truly_reduced" >> ${my_log}"ksm_pages_merged.log"
done
	
