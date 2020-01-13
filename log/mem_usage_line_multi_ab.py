import numpy as np
import matplotlib.pyplot as plt

# ab_mem.pdf
# 3
# 50
# ab-base/test_data/mem_usage.log
# 1578577865
# 1578577903
# Base
# ab-uksm/test_data/mem_usage.log
# 1578580636
# 1578580692
# UKSM
# ab-pksm200/test_data/mem_usage.log
# 1578578177
# 1578578220
# CKSM-50


X=[]
Y=[]
startStamp = []
startStampAB = []

filePath = []
lineLabel = []

colorTable = {'UKSM':'orange', 'Base':'royalblue', 'CKSM-50':'forestgreen', 'CKSM-100':'red', 'CKSM-200':'darkorchid', 'CKSM-500':'goldenrod'}



figFileName = input('figFileName: ')
lineNum = int(input('lineNum: '))
idxGap = 1
stopTime = int(input('stop: '))

for i in range(lineNum):
    filePath.append(input('file: '))
    startStamp.append(int(input('start: ')))
    startStampAB.append(int(input('startAB: ')))
    lineLabel.append(input('label: '))
    Y.append([])
    X.append([])

for i in range(lineNum):
    print(i)
    curFile = open(filePath[i], 'r')

    baseFree = 0
    idx = 0.0
    loaderStarted = False
    newFile = True

    while True:
        curLine = curFile.readline().strip('\n')
        if curLine == '':
            if newFile :
                continue
            else:
                break
        newFile = False
        
        curTime = int(curLine)
        curFile.readline()
        curLineArr = [x for x in curFile.readline().strip('\n').split(' ') if x]
        # print(curLineArr)
        curFree = int(curLineArr[2])/1024/1024
        curFile.readline()

        if loaderStarted == False:
            baseFree = curFree


        if curTime >= startStamp[i]:
            loaderStarted = True
            if curTime >= startStampAB[i]:
                Y[i].append(curFree-baseFree)
                X[i].append(idx)
                idx += 1

        if idx > stopTime:
            break

    curFile.close()

# idx = 0.0
# for i in range(len(Y[0])):
#     X.append(idx)
#     idx += idxGap

print(X)
print(Y)


plt.figure(figsize=(9,6))


# plt.figure()
for i in range(lineNum):
    plt.plot(X[i],Y[i], label=lineLabel[i], linewidth=4,marker='o',color=colorTable[lineLabel[i]])
    # plt.plot(X,Y[i], label=lineLabel[i], linewidth=4)

plt.legend()

# plt.set_size_inches(18.5, 10.5)

plt.xlabel('Time(s)')
plt.ylabel('Memory Usage(MB)')

plt.subplots_adjust(left=0.09, right=0.98, top=0.98, bottom=0.09)

plt.savefig(figFileName)

plt.show()