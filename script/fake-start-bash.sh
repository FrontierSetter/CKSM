echo > ${my_log}"timestamp_fake.log"

for ((i=1;i<=$1;i++))
do
    date +%s >> ${my_log}"timestamp_fake.log"
    virsh start "fake$i"

    # sleep $1
done