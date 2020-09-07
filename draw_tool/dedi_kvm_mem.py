import sys
import matplotlib.pyplot as plt

# python .\dedi_kvm_mem.py '..\log\8-12-2(kvm8_uksm)\out_mem_usage.log' '..\log\8-12-7(kvm8_ksm)\out_mem_usage.log' '..\log\8-12-6(kvm8_base)\out_mem_usage.log' '..\log\8-12-4(kvm8_pksm)\out_mem_usage.log'
# python .\dedi_kvm_mem.py '..\log\8-13-4(kvm25_base)\out_mem_usage.log' '..\log\8-13-7(kvm25_uksm)\out_mem_usage.log' '..\log\8-13-6(kvm25_ksm500)\out_mem_usage.log' '..\log\8-13-8(kvm25_pksm)\out_mem_usage.log'

markerTable = {'UKSM':'s', 'Base':'o', 'CKSM':'D', 'KSM':'^'}
colorTable = {'UKSM':'tab:orange', 'Base':'tab:blue', 'CKSM':'tab:green', 'KSM':'tab:olive'}


xArr = []
yArr = []
typeArr = []
compArr = []

totalContainerNum = 3

for i in range(1, len(sys.argv)):
    foundComp = False
    curFilePath = sys.argv[i]
    print(curFilePath)
    curFile = open(curFilePath, 'r')
    curType = curFile.readline().strip('\n')
    
    baseArr = curFile.readline().strip('\n').split(',')
    baseTime = int(baseArr[0])
    baseMem = int(baseArr[1])

    compTime = int(baseArr[2])
    scaleFactor = float(baseArr[3]) if len(baseArr) > 3 else 1
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
        curMem = int(curArr[1])

        if curTime < baseTime:
            continue
        
        xArr[i-1].append(int((curTime-baseTime)*scaleFactor))
        yArr[i-1].append(float(curMem-baseMem)/1024.0/1024.0/1024.0)

        if curTime >= compTime and foundComp == False:
            compArr.append(((curTime-baseTime), (float(curMem-baseMem)/1024.0/1024.0/1024.0)))
            foundComp = True

plt.figure(figsize=(9,6))

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
    plt.plot(xArr[i],yArr[i], label=typeArr[i], linewidth=4, marker=markerTable[typeArr[i]], color=colorTable[typeArr[i]], markevery=int(len(xArr[i])/15), markersize=10)
    # plt.annotate('', compArr[i],xytext=(compArr[i][0]-6, compArr[i][1]+0.6), arrowprops=dict(arrowstyle='-|>',connectionstyle='arc3',color='red'))

plt.legend(fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlabel('Time(s)', fontsize=24)
plt.ylabel('Memory Usage(GB)', fontsize=24)
plt.subplots_adjust(left=0.08, right=0.99, top=0.99, bottom=0.11)

plt.savefig('kvm_mem.pdf')

plt.show()



