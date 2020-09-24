import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

oriData = [
    # {
    #     'name': 'tomcat',
    #     'base': (6591991808, 6591991808),
    #     'cksm': (6117646336, 6087512064),
    #     'uksm': (6618267648, 6604619776)
    # },
    # {
    #     'name': 'redis',
    #     'base': (350236672, 321622016),
    #     'cksm': (334041088, 265355264),
    #     'uksm': (367796224, 296054784)
    # },
    # {
    #     'name': 'postgres',
    #     'base': (520278016, 492265472),
    #     'cksm': (515764224, 426946560),
    #     'uksm': (507772928, 492249088)
    # },
    # {
    #     'name': 'apache',
    #     'base': (532283392, 504754176),
    #     'cksm': (488484864, 455053312),
    #     'uksm': (571654144, 530747392)
    # },
    {
        'name': 'MongoDB$_{\\times64}$',
        'base': (4822536192, 4822253568),
        'cksm': (991703040, 871923712),
        'uksm': (1354911744, 1014169600),
        'CKSM-Full': (2129125376, 0),
        'KSM+': (2901811200, 0),
    },
    {
        'name': 'MySQL$_{\\times64}$',
        'base': (8211066880, 8098664448),
        'cksm': (3730710528, 2782498816),
        'uksm': (5361999872, 2849886208),
        'CKSM-Full': (6624202752, 0),
        'KSM+': (6818529280, 0),
    },
    {
        'name': 'Couchbase$_{\\times64}$',
        'base': (15242874880, 15235932160),
        'cksm': (9445933056, 9390149632),
        'uksm': (12370128896, 11549716480),
        'CKSM-Full': (13690822656, 0),
        'KSM+': (13973622784, 0),
    },
]

dataIdx = 0 

cksmArr = []
uksmArr = []
fullArr = []
ksmArr = []
tickArr = []

for dataDict in oriData:
    tickArr.append(dataDict['name'])
    curCKSM = dataDict['cksm'][dataIdx]
    curUKSM = dataDict['uksm'][dataIdx]
    curBase = dataDict['base'][dataIdx]
    curFull = dataDict['CKSM-Full'][dataIdx]
    curKSM = dataDict['KSM+'][dataIdx]
    cksmArr.append(float(curBase-curCKSM)/curBase*100)
    uksmArr.append(float(curBase-curUKSM)/curBase*100)
    fullArr.append(float(curBase-curFull)/curBase*100)
    ksmArr.append(float(curBase-curKSM)/curBase*100)

x=np.arange(len(tickArr))
width = 0.2
# width = 0.16
gap = 0.08*width

plt.figure(figsize=(9,6))

plt.bar(x-width*1-1.5*gap, ksmArr, width, color='tab:olive', label='KSM+', edgecolor='black', hatch='x')
plt.bar(x, uksmArr, width, color='tab:orange', label='UKSM', edgecolor='black', hatch='\\')
plt.bar(x+width*1+1.5*gap, cksmArr, width, color='tab:green', label='CKSM', edgecolor='black', hatch='/')

# plt.bar(x-width*1.5-1.5*gap, ksmArr, width, color='tab:olive', label='KSM+', edgecolor='black', hatch='x')
# plt.bar(x-width*0.5-0.5*gap, fullArr, width, color='tab:pink', label='CKSM-Full', edgecolor='black', hatch='-')
# plt.bar(x+width*0.5+0.5*gap, uksmArr, width, color='tab:orange', label='UKSM', edgecolor='black', hatch='\\')
# plt.bar(x+width*1.5+1.5*gap, cksmArr, width, color='tab:green', label='CKSM', edgecolor='black', hatch='/')

plt.ylabel('Peak Deduplication Rate(%)', fontsize=26)
plt.yticks(fontsize=20)

# xfmt = PercentFormatter(xmax=1, decimals=1)
# plt.gca().yaxis.set_major_formatter(xfmt)

plt.xticks(x,tickArr, fontsize=22)
plt.legend(fontsize=22, ncol=2)

plt.subplots_adjust(left=0.095, right=0.98, top=0.99, bottom=0.09)

plt.savefig('Peak_dedup_rate.pdf')
plt.show()