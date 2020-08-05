import sys
import matplotlib.pyplot as plt
import numpy as np

xArr = []
yArr = []
typeArr = []
compArr = []

totalContainerNum = 3
drawThreshold = 60.0

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

    xArr.append(curType)
    curTotalTime = 0.0
    curTotalCnt = 0

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

        if curTime > compTime:
            break

        curTotalCnt += 1
        curTotalTime += curOverhead 

    yArr.append(curTotalTime/curTotalCnt)
    print("type: %s, time: %f, cnt: %f" % (curType, curTotalTime, curTotalCnt))

plt.figure(figsize=(9,6))

barWidth = 0.5

x=np.arange(len(sys.argv)-1)
plt.bar(x, yArr, barWidth)
plt.xticks(x,xArr,fontsize=12)

plt.legend(fontsize=16)
# plt.xlabel('Time(s)', fontsize=18)
plt.ylabel('Overhead(ns)', fontsize=18)
plt.subplots_adjust(left=0.08, right=0.99, top=0.96, bottom=0.11)

plt.show()



