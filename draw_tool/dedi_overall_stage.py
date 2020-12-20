import matplotlib.pyplot as plt
import numpy as np

stageName = ['maintain', 'scan', 'search', 'merge']

hatchDict={'scan': '\\', 'search': '/', 'merge': 'x', 'maintain': 'o'}
# colorDict={'scan': '#f9c74f', 'search': '#e05780', 'merge': '#43aa8b', 'maintain': '#577590'}
# colorDict={'scan': '#00ABA9', 'search': '#F09609', 'merge': '#339933', 'maintain': '#E51400'}
colorDict={'scan': '#3cb9fc', 'search': '#ffc076', 'merge': '#87e885', 'maintain': '#fa8080'}
# colorDict={'scan': '#577590', 'search': '#f9c74f', 'merge': '#43aa8b', 'maintain': '#e05780'}

nameArr = ['KSM+', 'UKSM', 'CKSM']

stageDict = {
    'CKSM':{
        'scan':2.206257135,
        'search': 4.78553377,
        'merge':7.21325147,
        'maintain':3.062688524,
    },
    'UKSM':{
        'scan':4.445438350,
        'search': 4.947458895,
        'merge':6.449164804,
        'maintain':6.955521686,
    },
    'KSM+':{
        'scan':5.113913990,
        'search': 79.476011237,
        'merge':4.502308565,
        'maintain':5.927325839,
    },
}

plt.figure(figsize=(9,6))
plt.subplots_adjust(left=0.1, right=0.98, top=0.99, bottom=0.1)

ind = np.arange(len(nameArr))
plt.xticks(ind, nameArr, fontsize=24)
width = 0.5

plt.ylabel('Time(ns)', fontsize=26)
plt.yticks(fontsize=22)

baseArr = [0]*len(nameArr)
legendArr = []
legendEntryArr = []

for curStage in stageName:
    curArr = []
    for name in nameArr:
        curArr.append(stageDict[name][curStage])

    print(curArr)

    curP = plt.bar(ind, curArr, width, bottom=baseArr, color=colorDict[curStage], hatch=hatchDict[curStage], edgecolor='black', linewidth=1)

    legendArr.insert(0,curP)
    legendEntryArr.insert(0,curStage)

    for i in range(len(curArr)):
        baseArr[i] += curArr[i]

plt.legend(legendArr, legendEntryArr, fontsize=22)

plt.savefig('overall_stage.pdf')
plt.show()