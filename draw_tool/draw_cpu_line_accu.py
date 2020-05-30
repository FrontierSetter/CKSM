import sys
import matplotlib.pyplot as plt

xArr = []
yArr = []
typeArr = []


for i in range(1, len(sys.argv)):
    curFilePath = sys.argv[i]
    print(curFilePath)
    curFile = open(curFilePath, 'r')
    curType = curFile.readline().strip('\n')
    
    baseArr = curFile.readline().strip('\n').split(',')
    baseTime = int(baseArr[0])
    baseCPU = float(baseArr[1])

    curAccu = 0.0

    xArr.append([])
    yArr.append([])
    typeArr.append(curType)

    while True:
        curLine = curFile.readline().strip('\n')

        if curLine == "":
            break

        curArr = curLine.split(',')
        curTime = int(curArr[0])
        curCPU = float(curArr[1])

        if curTime < baseTime:
            continue
        
        xArr[i-1].append(curTime-baseTime)
        curAccu += (float(curCPU-baseCPU)/100.0)
        yArr[i-1].append(curAccu)

plt.figure(figsize=(9,6))

for i in range(len(sys.argv)-1):
    plt.plot(xArr[i],yArr[i], label=typeArr[i], linewidth=3)

plt.legend(fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Time(s)', fontsize=18)
plt.ylabel('Core*Sec', fontsize=18)
plt.subplots_adjust(left=0.08, right=0.99, top=0.96, bottom=0.11)

plt.show()



