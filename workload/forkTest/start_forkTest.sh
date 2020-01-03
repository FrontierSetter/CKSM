echo > "./timeStamp"

# date +%s >> "./timeStamp"
# top -d 0.5 | grep Xorg >> "./cpu_consumption"

date +%s >> "./timeStamp"
./forkTest.exe 10240 1000 5 1 &

sleep 1

date +%s >> "./timeStamp"
./forkTest.exe 10240 1000 5 2 &

sleep 1

date +%s >> "./timeStamp"
./forkTest.exe 10240 1000 5 3 &

sleep 1

date +%s >> "./timeStamp"
./forkTest.exe 10240 1000 5 4 &
