while true
do
    docker run --name=$1 -d ubuntu:15.10 /bin/sh -c "while true;do echo hello docker;sleep 1;done"
    sleep 3
    docker stop $1
    docker rm $1
    sleep 1
done