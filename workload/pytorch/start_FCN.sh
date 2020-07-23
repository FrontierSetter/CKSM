. FCN_3_7/bin/activate

my_log="./" 
name="FCN"
> ${my_log}"timestamp_FCN.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_FCN.log"

    python3 train.py &
    # sleep 1
    # docker run -d kibana:7.5.1
    # sleep 6
done

date +%s >> ${my_log}"timestamp_FCN.log"
