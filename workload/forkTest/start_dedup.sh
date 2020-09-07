my_log="./" 
> ${my_log}"timestamp_dedup.log"

date +%s >> ${my_log}"timestamp_dedup.log"
echo 1 > "/sys/kernel/mm/$1/run"