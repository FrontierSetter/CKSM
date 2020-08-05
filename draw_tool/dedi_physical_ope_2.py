import matplotlib.pyplot as plt
import numpy as np
import sys

# python .\dedi_physical_ope_2.py  '..\log\7-23-1(elastic10)\stage_stack.log' '..\log\7-18-2(uksm_elastic10)\out_total.log' '..\log\7-18-9(pksm_nginx64)\out_total.log' '..\log\7-18-10(uksm_nginx64)\out_total.log'

hatchDict={'scan': '\\\\', 'hash': '.', 'compare': 'o', 'merge': 'x', 'other': '//'}
colorDict={'scan': '#577590', 'hash': '#43aa8b', 'compare': '#90be6d', 'merge': '#f9c74f', 'other': '#f94144'}
groupName = ['ElasticSearch', 'Nginx']

groupNum = int((len(sys.argv)-1)/2)
print(groupNum)

plt.figure(figsize=(9,6))
plt.subplots_adjust(left=0.1, right=0.99, top=0.90, bottom=0.11)
width = 0.5
legendArr = []
legendEntryArr = []

unitCast = 1.0

for groupIdx in range(groupNum):
    nameArr = []
    entryArr = []
    oriDict = {}

    for i in [1,2]:
        foundComp = False
        curFilePath = sys.argv[groupIdx*2+i]
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


    ind = np.arange(len(nameArr))

    plt.subplot(100+groupNum*10+(groupIdx+1))

    plt.xticks(ind, nameArr, fontsize=16)

    plt.ylabel('time(ns)', fontsize=18)
    plt.yticks(fontsize=14)


    baseArr = [0]*len(allArr[entryArr[0]])


    for curEntry in allArr:
        curP = plt.bar(ind, allArr[curEntry], width, bottom=baseArr, color='white', hatch=hatchDict[curEntry], edgecolor=colorDict[curEntry], linewidth=3)
        if groupIdx == 0:
            legendArr.insert(0,curP)
            legendEntryArr.insert(0,curEntry)

        for i in range(len(allArr[curEntry])):
            baseArr[i] += allArr[curEntry][i]
    
    plt.title(groupName[groupIdx], loc='center', y=-0.12, fontsize=14)

plt.figlegend(legendArr, legendEntryArr,ncol=len(legendEntryArr), loc="upper center", fontsize=16)

plt.savefig('physical_operation.pdf')

plt.show()

