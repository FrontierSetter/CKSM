echo > ${my_log}"timestamp_kvm.log"

date +%s >> ${my_log}"timestamp_kvm.log"
virsh start test1
sleep 10
date +%s >> ${my_log}"timestamp_kvm.log"
virsh start test2
# sleep 5
# date +%s >> ${my_log}"timestamp_kvm.log"
# virsh start test3
