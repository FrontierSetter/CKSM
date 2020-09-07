echo > "./timeStamp"

date +%s >> "./timeStamp"
./forkTest.exe 262144 $1 1 &

date +%s >> "./timeStamp"
./forkTest.exe 262144 $1 2 &

date +%s >> "./timeStamp"
./forkTest.exe 262144 $1 3 &

date +%s >> "./timeStamp"
./forkTest.exe 262144 $1 4 &
