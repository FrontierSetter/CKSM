import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

oriData = [
    {
        'name': 'tomcat',
        'base': (6591991808, 6591991808),
        'cksm': (6117646336, 5837512064),
        'uksm': (6618267648, 6604619776),
        'KSM-style': (6088024064, 5836013568)
    },
    {
        'name': 'redis',
        'base': (350236672, 321622016),
        'cksm': (334041088, 240755264),
        'uksm': (367796224, 296054784),
        'KSM-style': (328916992, 240721920)
    },
    {
        'name': 'postgres',
        'base': (520278016, 492265472),
        'cksm': (515764224, 423246560),
        'uksm': (507772928, 492249088),
        'KSM-style': (0, 423235584)
    },
    {
        'name': 'apache',
        'base': (532283392, 504754176),
        'cksm': (488484864, 436253312),
        'uksm': (571654144, 530747392),
        'KSM-style': (0, 436199424)
    },
    # {
    #     'name': 'mongodb',
    #     'base': (4822536192, 4822253568),
    #     'cksm': (991703040, 871923712),
    #     'uksm': (1354911744, 1014169600)
    # },
    # {
    #     'name': 'mysql',
    #     'base': (8211066880, 8098664448),
    #     'cksm': (3730710528, 2782498816),
    #     'uksm': (5361999872, 2849886208)
    # },
    # {
    #     'name': 'coachbase',
    #     'base': (15242874880, 15235932160),
    #     'cksm': (9445933056, 9390149632),
    #     'uksm': (12370128896, 11549716480)
    # },
]

dataIdx = 1 

cksmArr = []
uksmArr = []
fullArr = []
tickArr = []

for dataDict in oriData:
    tickArr.append(dataDict['name'])
    curCKSM = dataDict['cksm'][dataIdx]
    curUKSM = dataDict['uksm'][dataIdx]
    curBase = dataDict['base'][dataIdx]
    curFull = dataDict['KSM-style'][dataIdx]
    cksmArr.append(float(curBase-curCKSM)/curBase*100)
    uksmArr.append(float(curBase-curUKSM)/curBase*100)
    fullArr.append(float(curBase-curFull)/curBase*100)

x=np.arange(len(tickArr))
width = 0.25

plt.figure(figsize=(9,6))

plt.bar(x-width*1.05, fullArr, width, color='tab:pink', label='KSM-style', edgecolor='black', hatch='-')
plt.bar(x, cksmArr, width, color='tab:green', label='CKSM', edgecolor='black', hatch='/')
plt.bar(x+width*1.05, uksmArr, width, color='tab:orange', label='UKSM', edgecolor='black', hatch='\\')

plt.ylabel('Stable Deduplication Rate(%)', fontsize=18)
plt.yticks(fontsize=16)

# xfmt = PercentFormatter(xmax=1, decimals=1)
# plt.gca().yaxis.set_major_formatter(xfmt)

plt.xticks(x,tickArr, fontsize=16)
plt.axhline(y=0,ls="-",c="black",linewidth=1)#添加水平直线
plt.legend(fontsize=16)

plt.subplots_adjust(left=0.09, right=0.98, top=0.98, bottom=0.09)

plt.savefig('Stable_dedup_rate.pdf')
plt.show()