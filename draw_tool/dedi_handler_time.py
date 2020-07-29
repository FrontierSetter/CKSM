import sys
import matplotlib.pyplot as plt

xArr = []
yArr = []
typeArr = []
compArr = []

totalContainerNum = 3
drawThreshold = 100.0

for i in range(1, len(sys.argv)):
    foundComp = False
    curFilePath = sys.argv[i]
    print(curFilePath)
    curFile = open(curFilePath, 'r')
    curType = curFile.readline().strip('\n')
    
    baseArr = curFile.readline().strip('\n').split(',')
    baseTime = int(baseArr[0])
    baseOverhead = float(baseArr[1])

    compTime = int(baseArr[2])
    # compTime += (float(compTime-baseTime)/(totalContainerNum-1.0))

    xArr.append([])
    yArr.append([])
    typeArr.append(curType)

    while True:
        curLine = curFile.readline().strip('\n')

        if curLine == "":
            break

        curArr = curLine.split(',')
        curTime = int(curArr[0])
        curOverhead = float(curArr[1])
        if curOverhead > drawThreshold:
            continue

        if curTime < baseTime:
            continue
        
        xArr[i-1].append(curTime-baseTime)
        yArr[i-1].append(float(curOverhead-baseOverhead))

        if curTime >= compTime and foundComp == False:
            compArr.append(((curTime-baseTime), (float(curOverhead-baseOverhead))))
            foundComp = True

plt.figure(figsize=(9,6))

for i in range(len(sys.argv)-1):
    plt.plot(xArr[i],yArr[i], label=typeArr[i], linewidth=3)
    plt.annotate('', compArr[i],xytext=(compArr[i][0]-6, compArr[i][1]+0.6), arrowprops=dict(arrowstyle='-|>',connectionstyle='arc3',color='red'))

plt.legend(fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Time(s)', fontsize=18)
plt.ylabel('Overhead(ns)', fontsize=18)
plt.subplots_adjust(left=0.08, right=0.99, top=0.96, bottom=0.11)

plt.show()



