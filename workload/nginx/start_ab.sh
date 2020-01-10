name="ab"
echo "" > ${my_log}"timestamp_ab.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_ab.log"
    # docker run --name="$name$i" -d ubuntu:15.10 /bin/sh -c "while true;do echo hello docker;sleep 1;done"
    ab -c 5 -n 5000 "192.168.198.159:80$i/path" &

    # 每秒接近一百次请求

    # sleep 1
done