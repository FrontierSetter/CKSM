my_log="./test_data/" 

> ${my_log}"meta_usage.log"

while true;
do
	/bin/sleep 1

	date +%s >> ${my_log}"meta_usage.log"
	echo 'uksm_node_vma' >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/uksm_node_vma/object_size >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/uksm_node_vma/objects >> ${my_log}"meta_usage.log"
    echo 'uksm_rmap_item' >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/uksm_rmap_item/object_size >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/uksm_rmap_item/objects >> ${my_log}"meta_usage.log"
    echo 'uksm_stable_node' >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/uksm_stable_node/object_size >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/uksm_stable_node/objects >> ${my_log}"meta_usage.log"
    echo 'uksm_tree_node' >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/uksm_tree_node/object_size >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/uksm_tree_node/objects >> ${my_log}"meta_usage.log"
    echo 'uksm_vma_slot' >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/uksm_vma_slot/object_size >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/uksm_vma_slot/objects >> ${my_log}"meta_usage.log"
done