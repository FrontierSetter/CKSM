my_log="./"
name="nginx"
echo "" > "timestamp_remote_nginx.log"
date +%s >> "timestamp_remote_nginx.log"

ssh l@192.168.122.60 "echo 123456 | sudo -S bash /home/l/script/start_nginx_batch.sh 1; echo 123456 | sudo -S bash /home/l/script/start_redis.sh 64" &&
ssh l@192.168.122.252 "echo 123456 | sudo -S bash /home/l/script/start_nginx_batch.sh 1; echo 123456 | sudo -S bash /home/l/script/start_redis.sh 64" &&
ssh l@192.168.122.124 "echo 123456 | sudo -S bash /home/l/script/start_nginx_batch.sh 1; echo 123456 | sudo -S bash /home/l/script/start_redis.sh 64" &&
ssh l@192.168.122.219 "echo 123456 | sudo -S bash /home/l/script/start_nginx_batch.sh 1; echo 123456 | sudo -S bash /home/l/script/start_redis.sh 64" &&
ssh l@192.168.122.7 "echo 123456 | sudo -S bash /home/l/script/start_nginx_batch.sh 1; echo 123456 | sudo -S bash /home/l/script/start_redis.sh 64" &&
ssh l@192.168.122.248 "echo 123456 | sudo -S bash /home/l/script/start_nginx_batch.sh 1; echo 123456 | sudo -S bash /home/l/script/start_redis.sh 64" &&
ssh l@192.168.122.94 "echo 123456 | sudo -S bash /home/l/script/start_nginx_batch.sh 1; echo 123456 | sudo -S bash /home/l/script/start_redis.sh 64" &&
ssh l@192.168.122.233 "echo 123456 | sudo -S bash /home/l/script/start_nginx_batch.sh 1; echo 123456 | sudo -S bash /home/l/script/start_redis.sh 64"