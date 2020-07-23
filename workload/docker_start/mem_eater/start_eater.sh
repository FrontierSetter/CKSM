my_log="./" 
name="eater"
> ${my_log}"timestamp_eater.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_eater.log"

    docker run -d --memory=2g valentinomiazzo/memory-eater
    sleep 2
done

date +%s >> ${my_log}"timestamp_eater.log"
