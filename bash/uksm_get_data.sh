ori_log="/sys/kernel/mm/uksm/"
my_log="./test_data/" 

echo "" > ${my_log}"uksm_pages_map_cnt.log"
echo "" > ${my_log}"uksm_zero_pages_map_cnt.log"

while true;
do
	sleep 0.1

	date +%s >> ${my_log}"uksm_pages_map_cnt.log"
	cat ${ori_log}"pages_merge_cnt" >> ${my_log}"uksm_pages_map_cnt.log"
	cat ${ori_log}"pages_truly_reduced" >> ${my_log}"uksm_pages_map_cnt.log"
	cat ${ori_log}"pages_not_reduced" >> ${my_log}"uksm_pages_map_cnt.log"

	date +%s >> ${my_log}"uksm_zero_pages_map_cnt.log"
	cat ${ori_log}"zero_pages_merge_cnt" >> ${my_log}"uksm_zero_pages_map_cnt.log"
	cat ${ori_log}"zero_pages_truly_reduced" >> ${my_log}"uksm_zero_pages_map_cnt.log"
	cat ${ori_log}"zero_pages_not_reduced" >> ${my_log}"uksm_zero_pages_map_cnt.log"



done
	
