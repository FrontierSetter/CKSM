for ((i=0;i<$1;i++))
do
    virsh destroy "test$i"
done