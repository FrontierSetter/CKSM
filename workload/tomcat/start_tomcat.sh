my_log="./" 
name="tomcat"
> ${my_log}"timestamp_tomcat.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_tomcat.log"

    docker run -d tomcat
    sleep 1
    # docker run -d kibana:7.5.1
    # sleep 6
done

date +%s >> ${my_log}"timestamp_tomcat.log"
