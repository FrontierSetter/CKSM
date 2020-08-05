import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

oriData = [
    {
        'name': '8',
        'cksm': (30.784, 1315496),
        'uksm': (12.587, 393886)
    },
    {
        'name': '16',
        'cksm': (58.616, 2415795),
        'uksm': (27.246, 741406)
    },
    {
        'name': '32',
        'cksm': (110.291, 4995349),
        'uksm': (48.26, 1795442)
    },
    {
        'name': '64',
        'cksm': (193.852, 9747375),
        'uksm': (107.409, 3554864)
    },
    {
        'name': '128',
        'cksm': (338.744, 18072313),
        'uksm': (227.657, 6091816)
    }
]


cksmArr = []
uksmArr = []
tickArr = []

for dataDict in oriData:
    tickArr.append(dataDict['name'])
    curCksmCpu = dataDict['cksm'][0]
    curCksmMerge = dataDict['cksm'][1]
    curUksmCpu = dataDict['uksm'][0]
    curUksmMerge = dataDict['uksm'][1]
    cksmArr.append(float(curCksmCpu)/curCksmMerge)
    uksmArr.append(float(curUksmCpu)/curUksmMerge)

print(cksmArr)
# print(tickArr)

x=np.arange(len(tickArr))
width = 0.4

plt.figure(figsize=(9,6))

plt.bar(x-width/2*1.05, cksmArr, width, color='tab:green', label='CKSM', edgecolor='black', hatch='/')
plt.bar(x+width/2*1.05, uksmArr, width, color='tab:orange', label='UKSM', edgecolor='black', hatch='\\')

plt.ylabel('CPU Consumption per Merge(core*s) ', fontsize=18)
plt.yticks(fontsize=16)
# plt.ylim(0,100)

xfmt = ScalarFormatter(useMathText=True)
xfmt.set_powerlimits((0, 0))
plt.gca().yaxis.set_major_formatter(xfmt)

plt.xticks(x,tickArr, fontsize=16)
plt.xlabel('Main Memory Capacity(GB)', fontsize=18)

plt.subplots_adjust(left=0.09, right=0.98, top=0.96, bottom=0.11)

plt.legend(fontsize=16)

plt.savefig('scal_cpu_merge.pdf')
plt.show()