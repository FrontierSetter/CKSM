import matplotlib.pyplot as plt
import numpy as np
import sys

# python .\dedi_partial_hash_stage.py '..\log\8-6-1(nginx_with_partial)\out_1.log' '..\log\8-6-2(nginx_no_partial)\out_1.log' '..\log\8-6-1(nginx_with_partial)\out_2.log' '..\log\8-6-2(nginx_no_partial)\out_2.log' '..\log\8-6-1(nginx_with_partial)\out_3.log' '..\log\8-6-2(nginx_no_partial)\out_3.log'
# python .\dedi_partial_hash_stage.py '..\log\8-6-3(nginx_with_partial)\out_1.log' '..\log\8-6-2(nginx_no_partial)\out_1.log' '..\log\8-6-3(nginx_with_partial)\out_2.log' '..\log\8-6-2(nginx_no_partial)\out_2.log' '..\log\8-6-3(nginx_with_partial)\out_3.log' '..\log\8-6-2(nginx_no_partial)\out_3.log'

hatchDict={'scan': '\\\\', 'hash': '||', 'compare': '//', 'merge': 'x', 'maintain': 'o'}
colorDict={'scan': '#f9c74f', 'hash': '#fe7f2d', 'compare': '#e05780', 'merge': '#43aa8b', 'maintain': '#577590'}
# colorDict={'scan': '#577590', 'hash': '#43aa8b', 'compare': '#90be6d', 'merge': '#f9c74f', 'other': '#f94144'}
groupName = ['Light load (1 collision)', 'Normal load (6 collisions)', 'Heavy load (12 collisions)']

# stageSeq = ['hash', 'compare', 'maintain', 'scan', 'merge']
stageSeq = ['maintain', 'scan', 'hash', 'compare', 'merge']

groupNum = int((len(sys.argv)-1)/2)
print(groupNum)

plt.figure(figsize=(9,6))
plt.subplots_adjust(left=0.08, right=0.98, top=0.88, bottom=0.13)
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
            allArr['maintain'] = []
            for curName in nameArr:
                if curEntry not in oriDict[curName]:
                    allArr['maintain'].append(0.0)
                else:
                    temOther = oriDict[curName][curEntry]
                    for k in oriDict[curName]:
                        if k == curEntry or k == 'cnt':
                            continue
                        else:
                            temOther -= oriDict[curName][k]
                    allArr['maintain'].append(temOther/unitCast/oriDict[curName]['cnt'])
        else:
            allArr[curEntry] = []
            for curName in nameArr:
                if curEntry not in oriDict[curName]:
                    allArr[curEntry].append(0.0)
                else:
                    allArr[curEntry].append(oriDict[curName][curEntry]/unitCast/oriDict[curName]['cnt'])

    print(allArr)

    ind = np.arange(len(nameArr))

    plt.subplot(100+groupNum*10+(groupIdx+1))

    plt.xticks(ind, nameArr, fontsize=17)

    if groupIdx == 0:
        plt.ylabel('Time(ns)', fontsize=22)
    plt.yticks(fontsize=18)
    plt.ylim(0, 14)


    baseArr = [0]*len(allArr[entryArr[0]])


    for curEntry in stageSeq:
        curP = plt.bar(ind, allArr[curEntry], width, bottom=baseArr, color=colorDict[curEntry], hatch=hatchDict[curEntry], edgecolor='black', linewidth=1)
        # curP = plt.bar(ind, allArr[curEntry], width, bottom=baseArr, color='white', hatch=hatchDict[curEntry], edgecolor=colorDict[curEntry], linewidth=3)
        if groupIdx == 0:
            legendArr.append(curP)
            legendEntryArr.append(curEntry)
            # legendArr.insert(0,curP)
            # legendEntryArr.insert(0,curEntry)

        for i in range(len(allArr[curEntry])):
            baseArr[i] += allArr[curEntry][i]
    
    plt.title(groupName[groupIdx], loc='center', y=-0.14, fontsize=15)

plt.figlegend(legendArr, legendEntryArr,ncol=len(legendEntryArr), loc="upper center", fontsize=19, columnspacing=0.8, handletextpad=0.3)

plt.savefig('partial_hash_stage.pdf')

plt.show()

