import sys
import matplotlib.pyplot as plt
import random

# python .\dedi_multimap_both.py '..\log\12-6-2(uksm_fork_docker_32)\out_mem_usage.log' '..\log\12-6-3(uksm_fork_kvm_32)\out_mem_usage.log'
# python .\dedi_multimap_both.py '..\log\12-6-3(uksm_fork_kvm_32)\out_mem_usage.log' '..\log\12-6-2(uksm_fork_docker_32)\out_mem_usage.log' '..\log\13-10-1(ksm_fork_kvm_32)\out_mem_usage.log' '..\log\13-10-3(ksm_fork_docker_32_2)\out_mem_usage.log'

markerTable = {'UKSM-KVM':'s','UKSM-Docker':'s','KSM-KVM':'^','KSM-Docker':'^'}
colorTable = {'UKSM-KVM':'#F79646','UKSM-Docker':'#F79646','KSM-KVM':'#1f497d','KSM-Docker':'#1f497d'}
lineTable = {'UKSM-KVM':'--','UKSM-Docker':'-','KSM-KVM':'--','KSM-Docker':'-'}


xArr = []
yArr = []
typeArr = []
compArr = []

preIdx = -1

totalContainerNum = 3

for i in range(1, len(sys.argv)):
    foundComp = False
    curFilePath = sys.argv[i]
    print(curFilePath)
    curFile = open(curFilePath, 'r')
    curType = curFile.readline().strip('\n')
    if 'Full' in curType:
        curType = 'KSM-style'
    
    baseArr = curFile.readline().strip('\n').split(',')
    baseTime = int(baseArr[0])
    baseMem = int(baseArr[1])

    compTime = int(baseArr[2])
    scaleFactor = float(baseArr[3]) if len(baseArr) > 3 else 1
    # compTime += (float(compTime-baseTime)/(totalContainerNum-1.0))

    xArr.append([])
    yArr.append([])
    typeArr.append(curType)

    meetFlag = False
    peakMem = -1

    while True:
        curLine = curFile.readline().strip('\n')

        if curLine == "":
            break

        curArr = curLine.split(',')
        curTime = int(curArr[0])
        curMem = int(curArr[1])

        if curTime < baseTime:
            continue

        if curTime - baseTime > 300000:
            break

        if not meetFlag:
            peakMem = curMem-baseMem
            meetFlag = True

        if int((curTime-baseTime)*scaleFactor) == preIdx:
            yArr[i-1][-1] = float(peakMem-curMem)/1024.0/1024.0/1024.0
        else:       
            xArr[i-1].append(int((curTime-baseTime)*scaleFactor))
            # yArr[i-1].append(float(curMem-baseMem)/1024.0/1024.0/1024.0)
            yArr[i-1].append(float(peakMem-curMem)/1024.0/1024.0/1024.0)

        if curTime >= compTime and foundComp == False:
            compArr.append(((curTime-baseTime), (float(peakMem-curMem)/1024.0/1024.0/1024.0)))
            foundComp = True

        preIdx = int((curTime-baseTime)*scaleFactor)

# maxLen = 0
# for arr in yArr:
#     if len(arr) > maxLen:
#         maxLen = len(arr)

# while len(yArr[0]) < 500:
#     yArr[0].append(yArr[0][-1]+random.uniform(-0.0001,0.0001))
#     xArr[0].append(xArr[0][-1]+1.3)

mainLen = 200

fig = plt.figure(figsize=(9,6))

print('peak')
for i in range(len(sys.argv)-1):
    curPeak = 0.0
    for curMem in yArr[i]:
        if curMem > curPeak:
            curPeak = curMem
    print(curPeak)


print('stable')
for i in range(len(sys.argv)-1):
    # print(len(xArr[i])/15)
    print(yArr[i][-1])
    mainLenCur = 0
    while mainLenCur < len(xArr[i]) and xArr[i][mainLenCur] < mainLen:
        mainLenCur += 1
    plt.plot(xArr[i][:mainLenCur],yArr[i][:mainLenCur], label=typeArr[i], linewidth=4, marker=markerTable[typeArr[i]], color=colorTable[typeArr[i]], markevery=int(len(xArr[i][:mainLenCur])/15), markersize=12, linestyle=lineTable[typeArr[i]])
    # plt.annotate('', compArr[i],xytext=(compArr[i][0]-6, compArr[i][1]+0.6), arrowprops=dict(arrowstyle='-|>',connectionstyle='arc3',color='red'))

# plt.axhline(y=0,ls=":",c="red",linewidth=4)#添加水平直线


plt.legend(fontsize=20, loc="upper left", handlelength=2.5)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Time(s)', fontsize=26)
plt.ylabel('Memory Deduplicated(GB)', fontsize=26)
plt.subplots_adjust(left=0.1, right=0.99, top=0.99, bottom=0.12)

left,bottom,width,height = 0.73,0.17,0.25,0.25
# left,bottom,width,height = 0.71,0.15,0.25,0.20
ax1 = fig.add_axes([left,bottom,width,height])
for i in range(len(sys.argv)-1):
    ax1.plot(xArr[i],yArr[i], label=typeArr[i], linewidth=2, marker=markerTable[typeArr[i]], color=colorTable[typeArr[i]], markevery=int(len(xArr[i])/5), markersize=6, linestyle=lineTable[typeArr[i]])


plt.savefig('multimap_all.pdf')

plt.show()




