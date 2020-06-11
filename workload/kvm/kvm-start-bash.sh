# echo > ${my_log}"timestamp_kvm.log"

for ((i=0;i<$1;i++))
do
    # date +%s >> ${my_log}"timestamp_kvm.log"
    virsh start "test$i"

    sleep $2
done