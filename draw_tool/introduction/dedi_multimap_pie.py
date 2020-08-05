import matplotlib.pyplot as plt
import numpy as np
import sys

# python .\dedi_multimap.py '..\log\7-18-10(uksm_nginx64)\out_total_multi.log' '..\log\7-19-1(uksm_scalability4)\out_total.log'

nameArr = []
entryArr = []
oriDict = {}

unitCast = 1.0

foundComp = False
curFilePath = sys.argv[1]
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

labelArr = []
dataArr = []

for curEntry in oriDict[curName]:
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
        labelArr.append(curEntry)
        dataArr.append(oriDict[curName][curEntry])

plt.figure(figsize=(9,6))

print(dataArr)
print(labelArr)

plt.pie(x=dataArr, 
    # labels=labelArr, 
    autopct='%.2f%%',
    startangle=90,
    wedgeprops = {'linewidth': 2, 'edgecolor':'green'},
    explode=[0,0.2],
    textprops = {'fontsize':25, 'color':'black'},
    )
plt.legend(labels=labelArr, fontsize=19)
plt.subplots_adjust(left=0.09, right=0.98, top=0.99, bottom=0.01)

# plt.title('multi-map proportion in linux-scala')
plt.savefig('multi_map_pie.pdf')
plt.show()

