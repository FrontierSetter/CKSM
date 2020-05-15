pksm_thread=`ps -ef | grep -v grep | grep pksm | awk '{print $2}'`
echo $pksm_thread
ps -o pid,psr,comm -p $pksm_thread