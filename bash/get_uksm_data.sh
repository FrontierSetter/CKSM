ori_log="/sys/kernel/mm/uksm/"
my_log="./test_data/" 

echo "" > ${my_log}"full_scans.log"
echo "" > ${my_log}"pages_shared.log"
echo "" > ${my_log}"pages_sharing.log"
echo "" > ${my_log}"pages_unshared.log"

while true;
do
	/bin/sleep 0.1

	date +%s >> ${my_log}"full_scans.log"
	cat ${ori_log}"full_scans" >> ${my_log}"full_scans.log"

	date +%s >> ${my_log}"pages_shared.log"
	cat ${ori_log}"pages_shared" >> ${my_log}"pages_shared.log"

	date +%s >> ${my_log}"pages_sharing.log"
	cat ${ori_log}"pages_sharing" >> ${my_log}"pages_sharing.log"

	date +%s >> ${my_log}"pages_unshared.log"
	cat ${ori_log}"pages_unshared" >> ${my_log}"pages_unshared.log"

done
	
