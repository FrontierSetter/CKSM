# docker stop $(docker ps -aq)
# docker rm $(docker ps -aq)

name="test"

for ((i=0;i<$1;i++))
do
    # str = "$name$i"
    echo "$name$i"
    ./start_docker.sh "$name$i" &
    sleep 1
done