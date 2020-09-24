import sys
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import FuncFormatter, ScalarFormatter


memX = [0]
memY = [0]
mergeX = [0]
mergeY = [0]
cowX = [0]
cowY = [0]

globalIdx = 0
gapOffset = 1
powerScal = 5
powerFactor = 10**powerScal

preIdx = 0

for i in range(1, len(sys.argv)):

    memFilePath = sys.argv[i]
    pathTuple = os.path.split(memFilePath)
    mergeFilePath = os.path.join(pathTuple[0], 'out_pksm_merged.log')
    CowFilePath = os.path.join(pathTuple[0], 'out_page_cowed.log')

    print(memFilePath)
    print(mergeFilePath)
    print(CowFilePath)

    memFile = open(memFilePath, 'r')
    mergeFile = open(mergeFilePath, 'r')
    cowFile = open(CowFilePath, 'r')

    # 从mem文件中获取公共数据
    curType = memFile.readline().strip('\n')

    baseArr = memFile.readline().strip('\n').split(',')
    baseTime = int(baseArr[0])
    baseMem = int(baseArr[1])

    compTime = int(baseArr[2])

    # 获取mem数据
    while True:
        curLine = memFile.readline().strip('\n')

        if curLine == "":
            break

        curArr = curLine.split(',')
        curTime = int(curArr[0])
        curMem = int(curArr[1])

        if curTime < baseTime:
            continue

        memX.append(float(curTime-baseTime+globalIdx)/60/60)
        memY.append(float(curMem-baseMem)/1024.0/1024.0/1024.0)
        
    # 获取merge数据
    while True:
        curLine = mergeFile.readline().strip('\n')

        if curLine == "":
            break

        curArr = curLine.split(',')
        curTime = int(curArr[0])
        curMerge = int(curArr[1])

        if curTime < baseTime:
            continue

        curIdx = int((curTime-baseTime+globalIdx)/1)

        if curIdx == preIdx:
            mergeY[-1] += float(curMerge)/powerFactor
        else:
            # mergeX.append(float(curTime-baseTime+globalIdx)/60/60)
            mergeX.append(float(curIdx)/60/60)
            mergeY.append(float(curMerge)/powerFactor)
        
        preIdx = curIdx
        

    # 获取cow数据
    while True:
        curLine = cowFile.readline().strip('\n')

        if curLine == "":
            break

        curArr = curLine.split(',')
        curTime = int(curArr[0])
        curCow = int(curArr[1])

        if curTime < baseTime:
            continue
        
        curIdx = int((curTime-baseTime+globalIdx)/1)
        
        if curIdx == preIdx:
            cowY[-1] += float(curCow)/powerFactor
        else:
            # cowX.append(float(curTime-baseTime+globalIdx)/60/60)
            cowX.append(float(curIdx)/60/60)
            cowY.append(float(curCow)/powerFactor)
        
        preIdx = curIdx

    globalIdx = memX[-1]*60*60+gapOffset
    


fig = plt.figure(figsize=(9,6))

axMem = fig.add_subplot(311)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
# axMerge = axMem.twinx()
axMerge = fig.add_subplot(312)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
axCow = fig.add_subplot(313)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# 画mem
axMem.plot(memX,memY, label='Memory Usage', linewidth=2)
axMem.set_ylabel('Memory Usage(GB)', fontsize=13)

# 画merge
width = 1.0/60/60
axMerge.bar(mergeX, mergeY, width, color='tab:green')
axMerge.set_ylabel('Pages Merged($x10^{%d}$)' % (powerScal), fontsize=13)
# xfmt = ScalarFormatter(useMathText=True)
# axMerge.yaxis.set_major_formatter(xfmt)
axMerge.set_ylim(0,1.5)
# axMerge.set_ylim(1e0,1e5)
# axMerge.set_yscale("log")

# 画cow
axCow.bar(cowX, cowY, width, color='tab:red')
axCow.set_ylabel('Pages Split($x10^{%d}$)' % (powerScal), fontsize=13)
axCow.set_ylim(0,1.5)
# xfmt = ScalarFormatter(useMathText=True)
# axCow.yaxis.set_major_formatter(xfmt)
# axCow.set_ylim(1e0,1e5)
# axCow.set_yscale("log")

plt.subplots_adjust(left=0.08, right=0.95, top=0.96, bottom=0.11)
# plt.yticks(fontsize=16)
# plt.xticks(fontsize=16)
plt.xlabel('Time(h)', fontsize=18)

# plt.savefig('real_server.pdf')

plt.show()



