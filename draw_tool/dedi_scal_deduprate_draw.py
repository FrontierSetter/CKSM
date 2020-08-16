import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

oriData = [
    {
        'name': '8',
        'base': (6283055104.00, 6269247488.00),
        'cksm': (2388156416.00, 2352033792.00),
        'uksm': (6107328512.00, 4862025728.00)
    },
    {
        'name': '16',
        'base': (13010956288.00, 13002407936.00),
        'cksm': (5193732096.00, 4725534720.00),
        'uksm': (11333578752.00, 10038775808.00)
    },
    {
        'name': '32',
        'base': (28770263040.00, 28755832832.00),
        'cksm': (11986653184.00, 10832793600.00),
        'uksm': (25881534464.00, 21530796032.00)
    },
    {
        'name': '64',
        'base': (57843224576.00, 57828114432.00),
        'cksm': (24050266112.00, 22438096896.00),
        'uksm': (48851648512.00, 44084379648.00)
    },
    {
        'name': '128',
        'base': (113402871808.00, 113187479552.00),
        'cksm': (48313876480.00, 44245983232.00),
        'uksm': (90445701120.00, 85847764992.00)
    }
]

cksmPeakArr = []
uksmPeakArr = []
tickArr = []

for dataDict in oriData:
    tickArr.append(dataDict['name'])
    curCKSM = dataDict['cksm'][0]
    curUKSM = dataDict['uksm'][0]
    curBase = dataDict['base'][0]
    cksmPeakArr.append(float(curBase-curCKSM)/curBase*100)
    uksmPeakArr.append(float(curBase-curUKSM)/curBase*100)

cksmStableArr = []
uksmStableArr = []

for dataDict in oriData:
    # tickArr.append(dataDict['name'])
    curCKSM = dataDict['cksm'][1]
    curUKSM = dataDict['uksm'][1]
    curBase = dataDict['base'][1]
    cksmStableArr.append(float(curBase-curCKSM)/curBase*100)
    uksmStableArr.append(float(curBase-curUKSM)/curBase*100)

# print(cksmArr)
# print(tickArr)
print(cksmStableArr)
print(uksmStableArr)
print(cksmPeakArr)
print(uksmPeakArr)

x=np.arange(len(tickArr))
width = 0.4

plt.figure(figsize=(9,6))

plt.plot(range(len(cksmStableArr)), cksmStableArr, color='tab:green', label="CKSM-Stable", linewidth=4, marker='D', markersize=9)
plt.plot(range(len(cksmPeakArr)), cksmPeakArr, color='tab:green', label="CKSM-Peak", linestyle='--', linewidth=4, marker='D', markersize=9)

plt.plot(range(len(uksmStableArr)), uksmStableArr, color='tab:orange', label="UKSM-stable", linewidth=4, marker='s', markersize=9)
plt.plot(range(len(uksmPeakArr)), uksmPeakArr, color='tab:orange', label="UKSM-Peak", linestyle='--', linewidth=4, marker='s', markersize=9)

plt.ylabel('Deduplication Rate(%)', fontsize=18)
plt.yticks(fontsize=16)
plt.ylim(0,100)

# xfmt = PercentFormatter(xmax=1, decimals=1)
# plt.gca().yaxis.set_major_formatter(xfmt)

plt.xticks(x,tickArr, fontsize=16)
plt.xlabel('Main Memory Capacity(GB)', fontsize=18)

plt.subplots_adjust(left=0.09, right=0.98, top=0.98, bottom=0.11)

plt.legend(fontsize=14, ncol=2, handlelength=4)

plt.savefig('scal_dedup_rate.pdf')
plt.show()