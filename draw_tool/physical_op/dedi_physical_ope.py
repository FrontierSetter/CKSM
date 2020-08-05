import matplotlib.pyplot as plt
import numpy as np
import sys

# python .\dedi_physical_ope.py  '..\log\7-23-1(elastic10)\stage_stack.log' '..\log\7-18-2(uksm_elastic10)\out_total.log' 

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
cksmArr = {}
uksmArr = {}

for curEntry in entryArr:
    if curEntry == 'cnt':
        continue
    elif curEntry == 'total':
        # allArr['other'] = []
        cksmArr['other'] = []
        uksmArr['other'] = []
        for curName in nameArr:
            if curEntry not in oriDict[curName]:
                if 'UKSM' in curName:
                    uksmArr['other'].append(0.0)
                elif 'CKSM' in curName:
                    cksmArr['other'].append(0.0)
                else:
                    print('wrong')

            else:
                temOther = oriDict[curName][curEntry]
                for k in oriDict[curName]:
                    if k == curEntry or k == 'cnt':
                        continue
                    else:
                        temOther -= oriDict[curName][k]
                # allArr['other'].append(temOther/unitCast/oriDict[curName]['cnt'])
                if 'UKSM' in curName:
                    uksmArr['other'].append(temOther/unitCast/oriDict[curName]['cnt'])
                elif 'CKSM' in curName:
                    cksmArr['other'].append(temOther/unitCast/oriDict[curName]['cnt'])
                else:
                    print('wrong')
    else:
        # allArr[curEntry] = []
        cksmArr[curEntry] = []
        uksmArr[curEntry] = []
        for curName in nameArr:
            if curEntry not in oriDict[curName]:
                # allArr[curEntry].append(0.0)
                if 'UKSM' in curName:
                    uksmArr[curEntry].append(0.0)
                elif 'CKSM' in curName:
                    cksmArr[curEntry].append(0.0)
                else:
                    print('wrong')
            else:
                # allArr[curEntry].append(oriDict[curName][curEntry]/unitCast/oriDict[curName]['cnt'])
                if 'UKSM' in curName:
                    uksmArr[curEntry].append(oriDict[curName][curEntry]/unitCast/oriDict[curName]['cnt'])
                elif 'CKSM' in curName:
                    cksmArr[curEntry].append(oriDict[curName][curEntry]/unitCast/oriDict[curName]['cnt'])
                else:
                    print('wrong')

plt.figure(figsize=(9,6))

ind = np.arange(len(nameArr)/2)
plt.xticks(ind, nameArr)

plt.ylabel('time(ns)')

width = 0.35

baseArr = [0]*len(cksmArr[entryArr[0]])
legendArr = []
legendEntryArr = []

for curEntry in cksmArr:
    curP = plt.bar(ind-width/2*1.1, cksmArr[curEntry], width, bottom=baseArr)
    legendArr.insert(0,curP)
    legendEntryArr.insert(0,curEntry)

    for i in range(len(cksmArr[curEntry])):
        baseArr[i] += cksmArr[curEntry][i]

baseArr = [0]*len(uksmArr[entryArr[0]])

for curEntry in uksmArr:
    curP = plt.bar(ind+width/2*1.1, uksmArr[curEntry], width, bottom=baseArr)

    for i in range(len(uksmArr[curEntry])):
        baseArr[i] += uksmArr[curEntry][i]

plt.legend(legendArr, legendEntryArr)

plt.show()

