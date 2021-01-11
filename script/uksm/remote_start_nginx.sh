#!/bin/bash
my_log="./"
name="nginx"
echo "" > ${my_log}"timestamp_remote_nginx.log"

ssh l@192.168.122.252 "echo 123456 | sudo -S /home/l/script/start_nginx_batch.sh 3"
sleep 1
ssh l@192.168.122.124 "echo 123456 | sudo -S /home/l/script/start_nginx_batch.sh 3"
sleep 1
ssh l@192.168.122.219 "echo 123456 | sudo -S /home/l/script/start_nginx_batch.sh 3"
sleep 1
ssh l@192.168.122.60 "echo 123456 | sudo -S /home/l/script/start_nginx_batch.sh 3"
sleep 1
ssh l@192.168.122.7 "echo 123456 | sudo -S /home/l/script/start_nginx_batch.sh 3"
sleep 1
ssh l@192.168.122.248 "echo 123456 | sudo -S /home/l/script/start_nginx_batch.sh 3"