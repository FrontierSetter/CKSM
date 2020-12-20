# docker stop $(docker ps -aq)
# docker rm $(docker ps -aq)

name="test"
echo "" > ${my_log}"timestamp.log"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
	date +%s >> ${my_log}"timestamp.log"
    # docker run --name="$name$i" -d ubuntu:15.10 /bin/sh -c "while true;do echo hello docker;sleep 1;done"
    docker run -d -p 80$i:80 -v /home/linux/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v /home/linux/nginx/log:/var/log/nginx -v /home/linux/nginx/html:/usr/share/nginx/html nginx

    httperf --server 127.0.0.1 --port 80$i --num-conns 2000 --rate 100 --timeout 2 &

    # ./start_docker.sh "$name$i" &
    sleep 1
done