import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

oriData = [
    {
        'name': '8',
        'cksm': (30.784, 1315496),
        'uksm': (12.587, 393886),
        'ksm': (98.222, 1058033),
    },
    {
        'name': '16',
        'cksm': (58.616, 2415795),
        'uksm': (27.246, 741406),
        'ksm': (200.876, 2111359),
    },
    {
        'name': '32',
        'cksm': (110.291, 4995349),
        'uksm': (48.26, 1795442),
        'ksm': (413.219, 4592299),
    },
    {
        'name': '64',
        'cksm': (193.852, 9747375),
        'uksm': (107.409, 3554864),
        'ksm': (968.769, 9156416),
    },
    {
        'name': '128',
        'cksm': (338.744, 18072313),
        'uksm': (227.657, 6091816),
        'ksm': (2144.705, 18309896),
    }
]


cksmArr = []
uksmArr = []
ksmArr = []
tickArr = []

for dataDict in oriData:
    tickArr.append(dataDict['name'])
    curCksmCpu = dataDict['cksm'][0]
    curCksmMerge = dataDict['cksm'][1]
    curUksmCpu = dataDict['uksm'][0]
    curUksmMerge = dataDict['uksm'][1]
    curKsmCpu = dataDict['ksm'][0]
    curKsmMerge = dataDict['ksm'][1]
    cksmArr.append(float(curCksmCpu)/curCksmMerge*100)
    uksmArr.append(float(curUksmCpu)/curUksmMerge*100)
    ksmArr.append(float(curKsmCpu)/curKsmMerge*100)

print(cksmArr)
# print(tickArr)

x=np.arange(len(tickArr))
width = 0.2
gap = 0.08*width

plt.figure(figsize=(9,6))

plt.bar(x-width-gap*1.5, ksmArr, width, color='tab:olive', label='KSM+', edgecolor='black', hatch='x')
plt.bar(x, uksmArr, width, color='tab:orange', label='UKSM', edgecolor='black', hatch='\\')
plt.bar(x+width+gap*1.5, cksmArr, width, color='tab:green', label='CKSM', edgecolor='black', hatch='/')

plt.ylabel('CPU Consumption(% core*s) ', fontsize=26)
plt.yticks(fontsize=20)
plt.ylim(0,0.0125)

xfmt = ScalarFormatter(useMathText=True)
xfmt.set_powerlimits((0, 0))
plt.gca().yaxis.set_major_formatter(xfmt)

# plt.text(0, 1.95, r'x 10$^{4}$',fontsize=20)

plt.xticks(x,tickArr, fontsize=20)
plt.xlabel('Main Memory Capacity(GB)', fontsize=26)

plt.subplots_adjust(left=0.105, right=0.99, top=0.96, bottom=0.13)

plt.legend(fontsize=22, ncol=3, loc='upper left', columnspacing=1)

plt.savefig('scal_cpu_merge.pdf')
plt.show()