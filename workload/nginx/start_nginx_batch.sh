my_log="./" 
name="nginx"
echo "" > ${my_log}"timestamp_nginx.log"

for ((i=0;i<$1;i++))
do
    echo "$name$i"
	date +%s >> ${my_log}"timestamp_nginx.log"
    docker run -d -p 80$i:80 -v /home/l/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v /home/l/nginx/log:/var/log/nginx -v /home/l/nginx/html:/usr/share/nginx/html nginx

    sleep 1
done