echo > ${my_log}"timestamp_kvm.log"

date +%s >> ${my_log}"timestamp_kvm.log"
virsh start test1
sleep 10
date +%s >> ${my_log}"timestamp_kvm.log"
virsh start test2
sleep 10
date +%s >> ${my_log}"timestamp_kvm.log"
virsh start test3
sleep 10
date +%s >> ${my_log}"timestamp_kvm.log"
virsh start test4

sleep 10
date +%s >> ${my_log}"timestamp_kvm.log"
virsh start test5
sleep 10
date +%s >> ${my_log}"timestamp_kvm.log"
virsh start test6
sleep 10
date +%s >> ${my_log}"timestamp_kvm.log"
virsh start test7
sleep 10
date +%s >> ${my_log}"timestamp_kvm.log"
virsh start test8

# sleep 5
# date +%s >> ${my_log}"timestamp_kvm.log"
# virsh start test3
