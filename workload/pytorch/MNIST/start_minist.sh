echo "" > ${my_log}"timestamp.log"

for ((i=0;i<$1;i++))
do
	date +%s >> ${my_log}"timestamp.log"
    python MINST_test.py $2 &
    # docker run --name="$name$i" -d ubuntu:15.10 /bin/sh -c "while true;do echo hello docker;sleep 1;done"
    sleep 1
done