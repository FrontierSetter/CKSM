my_log="./" 
name="mc"
> ${my_log}"timestamp_mc.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_mc.log"

    docker run -d -e EULA=TRUE -e MEMORY=6G -e SEED=1785852800490497919 itzg/minecraft-server

    sleep 2
    # docker run -d kibana:7.5.1
    # sleep 6
done

date +%s >> ${my_log}"timestamp_mc.log"
