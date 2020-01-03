ori_log="/sys/kernel/mm/pksm/"
my_log="./test_data/" 

echo "" > ${my_log}"pksm_pages_sharing.log"
echo "" > ${my_log}"pksm_pages_shared.log"
# echo "" > ${my_log}"cpu_consumption.log"


while true;
do
	sleep 0.1

	date +%s >> ${my_log}"pksm_pages_sharing.log"
	cat ${ori_log}"pages_sharing" >> ${my_log}"pksm_pages_sharing.log"
	cat ${ori_log}"pages_shared" >> ${my_log}"pksm_pages_shared.log"
done
	
