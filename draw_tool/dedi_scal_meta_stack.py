import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

# colorDict = {
#     'scan': '#2a9d8f', 
#     'pattern': '#e9c46a', 
#     'merged': '#f4a261'
# }

colorDict = {
    'scan': '#247ba0', 
    'pattern': '#ffe066', 
    'merged': '#f25f5c'
}

hatchDict = {
    'scan': '//', 
    'pattern': '\\\\', 
    'merged': 'x'
}

markerTable = {'UKSM':'s', 'Base':'o', 'CKSM':'D'}
colorTable = {'UKSM':'tab:orange', 'Base':'tab:blue', 'CKSM':'tab:green'}


stageNameArr = ['scan', 'pattern', 'merged']
tickArr = ['8','16','32','64','128']
dataScale = float(1024*1024)    # B->MB
memoryScale = float(1024*1024*1024)       # GB->B

oriData = [
    {
        'name': '8',
        'memory': 8,
        'cksm': {
            # 'scan': 80*430178,
            # 'pattern': 40*872643,
            # 'merged': 40*872643
            'scan': 80*423473,
            'pattern': 40*170828,
            'merged': 40*686833
        },
        'uksm': {
            # 'scan': 192*460152,             # uksm_vma_slot
            # 'pattern': 64*234496+72*31752,  # uksm_tree_node uksm_stable_node
            # 'merged': 80*217617+40*22848     # uksm_rmap_item uksm_node_vma
            'scan': 192*445094,             # uksm_vma_slot
            'pattern': 64*97921+72*481,  # uksm_tree_node uksm_stable_node
            'merged': 80*222903+40*11822     # uksm_rmap_item uksm_node_vma

        }
    },
    {
        'name': '16',
        'memory': 16,
        'cksm': {
            # 'scan': 80*833572,
            # 'pattern': 40*1722168,
            # 'merged': 40*1722168
            'scan': 80*831437,
            'pattern': 40*385427,
            'merged': 40*1355715
        },
        'uksm': {
            # 'scan': 192*898926,            
            # 'pattern': 64*458559+72*50512, 
            # 'merged': 80*409530+40*21318 
            'scan': 192*876667,             # uksm_vma_slot
            'pattern': 64*390189+72*958,  # uksm_tree_node uksm_stable_node
            'merged': 80*419403+40*10191     # uksm_rmap_item uksm_node_vma

        }
    },
    {
        'name': '32',
        'memory': 32,
        'cksm': {
            # 'scan': 80*1979004,
            # 'pattern': 40*3214254,
            # 'merged': 40*3214254
            'scan': 80*1930780,
            'pattern': 40*639799,
            'merged': 40*2731564
        },
        'uksm': {
            # 'scan': 192*1779224,            
            # 'pattern': 64*184256+72*88312,  926991
            # 'merged': 80*928098+40*26826 
            'scan': 192*1739741,             # uksm_vma_slot
            'pattern': 64*926991+72*1129,  # uksm_tree_node uksm_stable_node
            'merged': 80*976478+40*18095     # uksm_rmap_item uksm_node_vma
        }
    },
    {
        'name': '64',
        'memory': 64,
        'cksm': {
            # 'scan': 80*4285106,
            # 'pattern': 40*6735468,
            # 'merged': 40*6735774
            'scan': 80*4038004,
            'pattern': 40*1512379,
            'merged': 40*5400176
        },
        'uksm': {
            # 'scan': 192*3537261,            
            # 'pattern': 64*2124992+72*164192, 
            # 'merged': 80*1917753+40*28254 
            'scan': 192*3465016,             # uksm_vma_slot
            'pattern': 64*1828425+72*2625,  # uksm_tree_node uksm_stable_node
            'merged': 80*1917047+40*21929     # uksm_rmap_item uksm_node_vma

        }
    },
    {
        'name': '128',
        'memory': 128,
        'cksm': {
            # 'scan': 80*8320752,
            # 'pattern': 40*12754488,
            # 'merged': 40*12754590
            'scan': 80*8809826,
            'pattern': 40*2970230,
            'merged': 40*10021571
        },
        'uksm': {
            # 'scan': 192*7046615,            
            # 'pattern': 64*1001280+72*312704, 
            # 'merged': 80*2483853+40*42344 
            'scan': 192*6912191,             # uksm_vma_slot
            'pattern': 64*2124992+72*4909,  # uksm_tree_node uksm_stable_node
            'merged': 80*3775968+40*30765     # uksm_rmap_item uksm_node_vma

        }
    }
]

print(oriData)

# 获取柱状图数据
cksmArr = []
uksmArr = []

for stageName in stageNameArr:
    cksmArr.append([])
    uksmArr.append([])
    for dataDict in oriData:
        curCKSM = dataDict['cksm'][stageName]/dataScale
        curUKSM = dataDict['uksm'][stageName]/dataScale
        cksmArr[-1].append(curCKSM)
        uksmArr[-1].append(curUKSM)
print(cksmArr)
print(uksmArr)

# 获取折线图数据
cksmPercentArr = []
uksmPercentArr = []

for dataDict in oriData:
    curCksmTotal = 0
    curUksmTotal = 0
    curMemory = dataDict['memory']*memoryScale
    for stageName in stageNameArr:
        curCksmTotal += dataDict['cksm'][stageName]
        curUksmTotal += dataDict['uksm'][stageName]
    cksmPercentArr.append(curCksmTotal/curMemory*100)
    uksmPercentArr.append(curUksmTotal/curMemory*100)
print(cksmPercentArr)
print(uksmPercentArr)


x=np.arange(len(tickArr))
width = 0.4

fig = plt.figure(figsize=(9,6))
axBar = fig.add_subplot(111)
axPlot=axBar.twinx()



axPlot.plot(x-width/2*1.1,cksmPercentArr, label='CKSM', linewidth=4, marker=markerTable['CKSM'], color=colorTable['CKSM'], markersize=9)
axPlot.plot(x+width/2*1.1,uksmPercentArr, label='UKSM', linewidth=4, marker=markerTable['UKSM'], color=colorTable['UKSM'], markersize=9)
axPlot.set_ylim(0.5, 1.5)
axPlot.set_ylabel('Meta Data / Total Memory(%)', fontsize=18)
axPlot.legend(fontsize=16, loc='lower right')


legendArrBar = []
legendEntryArrBar = []

baseArr = [0]*len(cksmArr[0])

for curStageArr,curEntry in zip(cksmArr,stageNameArr):
    curP = axBar.bar(x-width/2*1.1, curStageArr, width, bottom=baseArr, color=colorDict[curEntry], hatch=hatchDict[curEntry],edgecolor='black', linewidth=1)
    legendArrBar.insert(0,curP)
    legendEntryArrBar.insert(0,curEntry)

    for i in range(len(curStageArr)):
        baseArr[i] += curStageArr[i]

baseArr = [0]*len(uksmArr[0])

for curStageArr,curEntry in zip(uksmArr,stageNameArr):
    curP = axBar.bar(x+width/2*1.1, curStageArr, width, bottom=baseArr, color=colorDict[curEntry], hatch=hatchDict[curEntry],edgecolor='black', linewidth=1)

    for i in range(len(curStageArr)):
        baseArr[i] += curStageArr[i]

axBar.set_ylabel('Meta Data Usage(MB)', fontsize=18)
axBar.legend(legendArrBar, legendEntryArrBar, fontsize=16)
axBar.set_xticks(x)
axBar.set_xticklabels(tickArr, fontsize=16)
axBar.set_xlabel('Main Memory Capacity(GB)', fontsize=18)

plt.subplots_adjust(left=0.1, right=0.9, top=0.98, bottom=0.11)
plt.yticks(fontsize=16)

plt.savefig('scal_meta_stage_bar.pdf')
plt.show()