import numpy as np
import matplotlib.pyplot as plt

# overcommit.pdf
# 3
# 5000
# nginx256-4g-base/test_data/mem_usage.log
# 1578821123
# Base
# nginx256-4g-base/test_data/mem_usage.log
# 1578821123
# Base-Swap
# nginx256-4g-pksm100/test_data/mem_usage.log
# 1578819454
# CKSM-50



X=[]
Y=[]
startStamp = []
filePath = []
lineLabel = []

colorTable = {'UKSM':'orange', 'Base':'royalblue', 'Base-Swap':'royalblue', 'CKSM-50':'forestgreen', 'CKSM-100':'red', 'CKSM-200':'darkorchid', 'CKSM-500':'goldenrod', 'KSM-100':'yellow'}


figFileName = input('figFileName: ')
lineNum = int(input('lineNum: '))
idxGap = 1
stopTime = int(input('stop: '))

for i in range(lineNum):
    filePath.append(input('file: '))
    startStamp.append(int(input('start: ')))
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
        
        if 'Swap' in lineLabel[i]:
            curFile.readline()
            curLineArr = [x for x in curFile.readline().strip('\n').split(' ') if x]
            # print(curLineArr)
            curFree = int(curLineArr[2])/1024/1024
        else:
            curLineArr = [x for x in curFile.readline().strip('\n').split(' ') if x]
            # print(curLineArr)
            curFree = int(curLineArr[2])/1024/1024
            curFile.readline()

        if loaderStarted == False:
            baseFree = curFree


        if curTime >= startStamp[i]:
            if loaderStarted == False or ('Base' in lineLabel[i] and curFree-baseFree-preFree < 30) or ('CKSM' in lineLabel[i] and curFree-baseFree-preFree < 17):
                loaderStarted = True
                Y[i].append(curFree-baseFree)
                X[i].append(idx)
                preFree = curFree-baseFree

                if 'Swap' in lineLabel[i] and Y[i][-1] == 0:
                    Y[i].pop()
                    X[i].pop()

            idx += 1

        if idx > stopTime:
            break

    curFile.close()

# idx = 0.0
# for i in range(len(Y[0])):
#     X.append(idx)
#     idx += idxGap

print(X[1])
print(Y[1])

for i in range(lineNum):
    print(lineLabel[i])
    print(Y[i][-1])


plt.figure(figsize=(9,6))


# plt.figure()
for i in range(lineNum):
    print(i)
    if i == 1:
        print(lineLabel[i])
        plt.plot(X[i],Y[i], label=lineLabel[i], linewidth=4,color=colorTable[lineLabel[i]], linestyle="--")
    else:
        plt.plot(X[i],Y[i], label=lineLabel[i], linewidth=4,color=colorTable[lineLabel[i]])
    # plt.plot(X[i],Y[i], label=lineLabel[i], linewidth=4,marker='o',color=colorTable[lineLabel[i]])
    # plt.plot(X,Y[i], label=lineLabel[i], linewidth=4)

plt.legend()

# plt.set_size_inches(18.5, 10.5)

plt.xlabel('Time(s)')
plt.ylabel('Memory Usage(MB)')
plt.subplots_adjust(left=0.09, right=0.98, top=0.98, bottom=0.09)

plt.savefig(figFileName)

plt.show()