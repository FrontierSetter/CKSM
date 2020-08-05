import sys

curFilePath = sys.argv[1]
print(curFilePath)
curFile = open(curFilePath, 'r')
curType = curFile.readline().strip('\n')

baseArr = curFile.readline().strip('\n').split(',')
baseTime = int(baseArr[0])
baseCPU = float(baseArr[1])
compTime = int(baseArr[2])
lastTime = baseTime-1

curAccu = 0.0

while True:
    curLine = curFile.readline().strip('\n')

    if curLine == "":
        break

    curArr = curLine.split(',')
    curTime = int(curArr[0])
    curCPU = float(curArr[1])

    if curTime < baseTime:
        continue

    if curTime-lastTime != 1:
        print("gap %d" % (curTime-lastTime))
    
    curAccu += (float(curCPU-baseCPU)/100.0*(curTime-lastTime))
    lastTime = curTime

    if curTime > compTime:
        break

print("CPU: %f" % (curAccu))