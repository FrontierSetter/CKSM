perf probe 'perf_break_point group_number point_number'

mem_usage=`free -g | grep Mem | awk '{print $3}'`
pksm_thread=`ps -ef | grep -v grep | grep pksm | awk '{print $2}'`
echo $pksm_thread

while (($mem_usage < $1))
do
    echo $mem_usage
    mem_usage=`free -g | grep Mem | awk '{print $3}'`
    sleep 1
done

date +%s > start.timestamp
perf record -e probe:perf_break_point -a -c 1 -p $pksm_thread sleep $2