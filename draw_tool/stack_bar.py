import matplotlib.pyplot as plt
import numpy as np
import sys

nameArr = []
entryArr = []
oriDict = {}

unitCast = 1.0

for i in range(1, len(sys.argv)):
    foundComp = False
    curFilePath = sys.argv[i]
    print(curFilePath)
    curFile = open(curFilePath, 'r')

    curName = curFile.readline().strip('\n').split()[1]
    if curName in oriDict:
        print("wrong, %s duplicate" % (curName))
    else:
        nameArr.append(curName)

    oriDict[curName] = {}
    
    while True:
        curLine = curFile.readline()
        if curLine == "":
            break

        curArr = curLine.strip('\n').split()
        curEntry = curArr[0]

        if curEntry == '#':
            continue

        curValue = int(curArr[1])

        if curEntry not in entryArr:
            entryArr.append(curEntry)

        if curEntry not in oriDict[curName]:
            oriDict[curName][curEntry] = curValue
        else:
            oriDict[curName][curEntry] += curValue

    curFile.close()

print(oriDict)

allArr = {}

for curEntry in entryArr:
    if curEntry == 'cnt':
        continue
    elif curEntry == 'total':
        allArr['other'] = []
        for curName in nameArr:
            if curEntry not in oriDict[curName]:
                allArr['other'].append(0.0)
            else:
                temOther = oriDict[curName][curEntry]
                for k in oriDict[curName]:
                    if k == curEntry or k == 'cnt':
                        continue
                    else:
                        temOther -= oriDict[curName][k]
                allArr['other'].append(temOther/unitCast/oriDict[curName]['cnt'])
    else:
        allArr[curEntry] = []
        for curName in nameArr:
            if curEntry not in oriDict[curName]:
                allArr[curEntry].append(0.0)
            else:
                allArr[curEntry].append(oriDict[curName][curEntry]/unitCast/oriDict[curName]['cnt'])

plt.figure(figsize=(9,6))

ind = np.arange(len(nameArr))
plt.xticks(ind, nameArr)

plt.ylabel('time(ns)')

width = 0.35

baseArr = [0]*len(allArr[entryArr[0]])
legendArr = []
legendEntryArr = []

for curEntry in allArr:
    curP = plt.bar(ind, allArr[curEntry], width, bottom=baseArr)
    legendArr.insert(0,curP)
    legendEntryArr.insert(0,curEntry)

    for i in range(len(allArr[curEntry])):
        baseArr[i] += allArr[curEntry][i]

plt.legend(legendArr, legendEntryArr)

plt.show()

