my_log="./test_data/" 

> ${my_log}"meta_usage.log"

while true;
do
	/bin/sleep 1

	date +%s >> ${my_log}"meta_usage.log"
	echo 'page_slot' >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/pksm_page_slot/object_size >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/pksm_page_slot/objects >> ${my_log}"meta_usage.log"
    echo 'pksm_hash_node' >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/pksm_pksm_hash_node/object_size >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/pksm_pksm_hash_node/objects >> ${my_log}"meta_usage.log"
    echo 'pksm_rmap_item' >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/pksm_pksm_rmap_item/object_size >> ${my_log}"meta_usage.log"
    cat /sys/kernel/slab/pksm_pksm_rmap_item/objects >> ${my_log}"meta_usage.log"
done