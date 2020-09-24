import sys
import matplotlib.pyplot as plt

# noKSM
# python dedi_scal_mem.py '..\log\7-29-1(large_128_base)\out_mem_usage.log' '..\log\7-29-2(large_128_uksm)\out_mem_usage.log' '..\log\7-29-3(large_128_pksm)\out_mem_usage.log'
# python .\dedi_scal_mem.py '..\log\7-29-6(large_64_base)\out_mem_usage.log' '..\log\7-29-5(large_64_uksm)\out_mem_usage.log' '..\log\7-29-4(large_64_pksm)\out_mem_usage.log'
# python .\dedi_scal_mem.py '..\log\7-29-10(large_32_base)\out_mem_usage.log' '..\log\7-29-9(large_32_uksm)\out_mem_usage.log' '..\log\7-29-8(large_32_pksm)\out_mem_usage.log'

# with KSM+
# python .\dedi_scal_mem.py '..\log\8-4-7(large8_base)\out_mem_usage.log' '..\log\8-29-4(large8_ksm5000)\out_mem_usage.log' '..\log\8-4-11(large8_uksm)\out_mem_usage.log' '..\log\8-4-3(large8_pksm)\out_mem_usage.log'
# python .\dedi_scal_mem.py '..\log\8-4-6(large16_base)\out_mem_usage.log' '..\log\8-4-2(large16_pksm)\out_mem_usage.log' '..\log\8-4-10(large16_uksm)\out_mem_usage.log' '..\log\8-29-3(large16_ksm5000)\out_mem_usage.log'
# python .\dedi_scal_mem.py '..\log\7-29-10(large_32_base)\out_mem_usage.log' '..\log\8-29-2(large32_ksm5000)\out_mem_usage.log' '..\log\7-29-9(large_32_uksm)\out_mem_usage.log' '..\log\7-29-8(large_32_pksm)\out_mem_usage.log'
# python .\dedi_scal_mem.py '..\log\7-29-6(large_64_base)\out_mem_usage.log' '..\log\8-29-5(large64_ksm5000)\out_mem_usage.log' '..\log\7-29-5(large_64_uksm)\out_mem_usage.log' '..\log\7-29-4(large_64_pksm)\out_mem_usage.log'
# python .\dedi_scal_mem.py '..\log\7-29-1(large_128_base)\out_mem_usage.log' '..\log\8-29-6(large128_ksm5000)\out_mem_usage.log' '..\log\7-29-2(large_128_uksm)\out_mem_usage.log' '..\log\7-29-3(large_128_pksm)\out_mem_usage.log'


markerTable = {'UKSM':'s', 'Base':'o', 'CKSM':'D', 'KSM+':'^', 'CKSM-Full':'d'}
colorTable = {'UKSM':'tab:orange', 'Base':'tab:blue', 'CKSM':'tab:green', 'KSM+':'tab:olive', 'CKSM-Full':'tab:pink'}


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

for i in range(len(sys.argv)-1):
    print(len(xArr[i])/15)
    plt.plot(xArr[i],yArr[i], label=typeArr[i], linewidth=4, marker=markerTable[typeArr[i]], color=colorTable[typeArr[i]], markevery=int(len(xArr[i])/15), markersize=9)
    # plt.annotate('', compArr[i],xytext=(compArr[i][0]-6, compArr[i][1]+0.6), arrowprops=dict(arrowstyle='-|>',connectionstyle='arc3',color='red'))

plt.legend(fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel('Time(s)', fontsize=18)
plt.ylabel('Memory Usage(GB)', fontsize=18)
plt.subplots_adjust(left=0.08, right=0.99, top=0.96, bottom=0.11)

# plt.savefig('scal_mem.pdf')

plt.show()



