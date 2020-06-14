pksm_thread=`ps -ef | grep -v grep | grep pksm | awk '{print $2}'`

A=("last_merged" "last_unmerged")
B=("full_scans" "scan_step" "pages_sharing" "pages_shared" "pages_inlist")

SETCOLOR_GREEN="echo -en \\033[1;32m"
SETCOLOR_RED="echo -en \\033[1;31m"
SETCOLOR_YELLOW="echo -en \\033[1;33m"
SETCOLOR_NORMAL="echo -en \\033[0m"

for x in ${A[@]};
do
    $SETCOLOR_GREEN && echo "${x} = $(cat /sys/kernel/mm/pksm/${x})" && $SETCOLOR_NORMAL
done

for x in ${B[@]};
do
    $SETCOLOR_YELLOW && echo "${x} = $(cat /sys/kernel/mm/pksm/${x})" && $SETCOLOR_NORMAL
done

find "/sys/kernel/mm/pksm/" -type f | while read x; do echo "$(basename ${x}) = $(cat ${x})"; done

$SETCOLOR_RED && top -b -p $pksm_thread -n 1 -d 1 && $SETCOLOR_NORMAL


# x='run'
# echo "${x} = $(cat /sys/kernel/mm/ksm/${x})"