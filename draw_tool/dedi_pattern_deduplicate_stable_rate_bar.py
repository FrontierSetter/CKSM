import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

oriData = [
    {
        'name': 'Redis$_{\\times64}$',
        'base': (350236672, 321622016),
        'cksm': (334041088, 240755264),
        'uksm': (367796224, 296054784),
        'CKSM-Full': (328916992, 240721920),
        'KSM+': (279851008, 238952448),
    },
    {
        'name': 'Tomcat$_{\\times64}$',
        'base': (6591991808, 6591991808),
        'cksm': (6117646336, 5837512064),
        'uksm': (6543306752, 6522470400),
        'CKSM-Full': (6088024064, 5836013568),
        'KSM+': (6067150848, 5932249088),
    },
    {
        'name': 'PostgreSQL$_{\\times64}$',
        'base': (520278016, 492265472),
        'cksm': (515764224, 423246560),
        'uksm': (507772928, 492249088),
        'CKSM-Full': (0, 423235584),
        'KSM+': (454070272, 415399936),
    },
    {
        'name': 'httpd$_{\\times64}$',
        'base': (532283392, 504754176),
        'cksm': (488484864, 436253312),
        'uksm': (538693632, 504545280),
        'CKSM-Full': (0, 436199424),
        'KSM+': (464302080, 433374848),
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

plt.bar(x-width*1-1.5*gap, ksmArr, width, edgecolor='#C00000', label='KSM+', color='white', hatch='xxxx', linewidth=2)
plt.bar(x, uksmArr, width, edgecolor='#F79646', label='UKSM', color='white', hatch='\\\\\\\\', linewidth=2)
plt.bar(x+width*1+1.5*gap, cksmArr, width, edgecolor='#1f497d', label='CKSM', color='white', hatch='////', linewidth=2)

# plt.bar(x-width*1.5-1.5*gap, ksmArr, width, color='tab:olive', label='KSM+', edgecolor='black', hatch='x')
# plt.bar(x-width*0.5-0.5*gap, fullArr, width, color='tab:pink', label='CKSM-Full', edgecolor='black', hatch='-')
# plt.bar(x+width*0.5+0.5*gap, uksmArr, width, color='tab:orange', label='UKSM', edgecolor='black', hatch='\\')
# plt.bar(x+width*1.5+1.5*gap, cksmArr, width, color='tab:green', label='CKSM', edgecolor='black', hatch='/')

plt.ylabel('Stable Deduplication Rate(%)', fontsize=26)
plt.yticks(fontsize=20)

# xfmt = PercentFormatter(xmax=1, decimals=1)
# plt.gca().yaxis.set_major_formatter(xfmt)

plt.xticks(x,tickArr, fontsize=22)
# plt.axhline(y=0,ls="-",c="black",linewidth=1)#添加水平直线
plt.legend(fontsize=22, ncol=2, loc='upper right')
# plt.legend(fontsize=20, ncol=2, loc='lower left')

plt.subplots_adjust(left=0.095, right=0.98, top=0.99, bottom=0.09)

plt.savefig('Stable_dedup_rate.pdf')
plt.show()