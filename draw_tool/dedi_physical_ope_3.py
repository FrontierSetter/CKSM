import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import sys

# python .\dedi_physical_ope_3.py  '..\log\7-23-1(elastic10)\stage_stack.log' '..\log\7-18-2(uksm_elastic10)\out_total.log' '..\log\8-26-12(ksm10000_elastic10)\out_total.log' '..\log\8-26-6(pksm_nginx32)\out_total.log' '..\log\8-26-9(uksm_nginx32)\out_total.log' '..\log\8-26-11(ksm10000_nginx32)\out_total.log' 
# python .\dedi_physical_ope_3.py  '..\log\7-23-1(elastic10)\stage_stack.log' '..\log\7-18-2(uksm_elastic10)\out_total.log' '..\log\8-26-12(ksm10000_elastic10)\out_total.log' '..\log\8-26-6(pksm_nginx32)\out_total.log' '..\log\8-26-9(uksm_nginx32)\out_total.log' '..\log\8-26-11(ksm10000_nginx32)\out_total.log'
# python .\dedi_physical_ope_3.py  '..\log\7-23-1(elastic10)\stage_stack_merge.log' '..\log\7-18-2(uksm_elastic10)\out_total_merge.log' '..\log\8-26-12(ksm10000_elastic10)\out_total_merge.log' '..\log\8-26-6(pksm_nginx32)\out_total_merge.log' '..\log\8-26-9(uksm_nginx32)\out_total_merge.log' '..\log\8-26-11(ksm10000_nginx32)\out_total_merge.log'

hatchDict={'scan': '\\\\', 'hash': '.', 'compare': 'o', 'merge': 'x', 'other': '//'}
colorDict={'scan': '#577590', 'hash': '#43aa8b', 'compare': '#90be6d', 'merge': '#f9c74f', 'other': '#f94144'}
groupName = ['Elasticsearch', 'Nginx']

barPerGroup = 3

groupNum = int((len(sys.argv)-1)/barPerGroup)
print(groupNum)

plt.figure(figsize=(9,6))
plt.subplots_adjust(left=0.09, right=0.95, top=0.9, bottom=0.12)

gs = gridspec.GridSpec(4,2, hspace=0.1)


width = 0.5
legendArr = []
legendEntryArr = []

unitCast = 1.0

for groupIdx in range(groupNum):
    nameArr = []
    entryArr = []
    oriDict = {}

    for i in range(1, barPerGroup+1):
        foundComp = False
        curFilePath = sys.argv[groupIdx*barPerGroup+i]
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

    print(allArr)

    ind = np.arange(len(nameArr))

    if groupIdx == 1:
        ax = plt.subplot(gs[1:,groupIdx])

        ax2 = plt.subplot(gs[0,groupIdx], sharex = ax)
        plt.yticks(fontsize=18)

        ax = plt.subplot(gs[1:,groupIdx])
        ax.spines['top'].set_visible(False)
        ax2.spines['bottom'].set_visible(False)
        ax2.axes.get_xaxis().set_visible(False)

        ax.set_ylim(0,72)
        ax2.set_ylim(578,602)

        d = 0.02  # 断层线的大小
        kwargs = dict(transform=ax2.transAxes, color='black', clip_on=False)
        ax2.plot((-d, +d), (-d*3, +d*3), **kwargs)        # top-left diagonal

        kwargs.update(transform=ax.transAxes)  # switch to the bottom axes
        ax.plot((-d, +d), (1-d, 1+d), **kwargs)  # bottom-left diagonal

        plt.title(groupName[groupIdx], loc='center', y=-0.20, fontsize=24)

    elif groupIdx == 0:
        ax = plt.subplot(gs[0:,groupIdx])
        plt.title(groupName[groupIdx], loc='center', y=-0.15, fontsize=24)

    plt.xticks(ind, nameArr, fontsize=20)

    plt.yticks(fontsize=18)

    if groupIdx == 0:
        plt.ylabel('Time(ns)', fontsize=24)


    baseArr = [0]*len(allArr[entryArr[0]])


    for curEntry in allArr:
        # curP = plt.bar(ind, allArr[curEntry], width, bottom=baseArr, color='white', hatch=hatchDict[curEntry], edgecolor=colorDict[curEntry], linewidth=3)
        if groupIdx == 1:
            curP = ax.bar(ind, allArr[curEntry], width, bottom=baseArr, color='white', hatch=hatchDict[curEntry], edgecolor=colorDict[curEntry], linewidth=3)
            ax2.bar(ind, allArr[curEntry], width, bottom=baseArr, color='white', hatch=hatchDict[curEntry], edgecolor=colorDict[curEntry], linewidth=3)
            legendArr.append(curP)
            legendEntryArr.append(curEntry)
            # legendArr.insert(0,curP)
            # legendEntryArr.insert(0,curEntry)
        else:
            curP = ax.bar(ind, allArr[curEntry], width, bottom=baseArr, color='white', hatch=hatchDict[curEntry], edgecolor=colorDict[curEntry], linewidth=3)


        for i in range(len(allArr[curEntry])):
            baseArr[i] += allArr[curEntry][i]
    

plt.figlegend(legendArr, legendEntryArr,ncol=len(legendEntryArr), loc="upper center", fontsize=16)

plt.savefig('physical_operation.pdf')

plt.show()

