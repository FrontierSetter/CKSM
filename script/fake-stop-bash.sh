for ((i=1;i<=$1;i++))
do
    virsh destroy "fake$i"
done