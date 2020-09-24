import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

oriData = [
    {
        'name': '8',
        'base': (6283055104.00, 6269247488.00),
        'cksm': (2388156416.00, 2352033792.00),
        'uksm': (6107328512.00, 4862025728.00),
        'ksm' : (5226938368.00, 2134413312.00)
    },
    {
        'name': '16',
        'base': (13010956288.00, 13002407936.00),
        'cksm': (5193732096.00, 4725534720.00),
        'uksm': (11333578752.00, 10038775808.00),
        'ksm' : (10722349056.00, 4401180672.00)
    },
    {
        'name': '32',
        'base': (28770263040.00, 28755832832.00),
        'cksm': (11986653184.00, 10832793600.00),
        'uksm': (25881534464.00, 21530796032.00),
        'ksm' : (25242664960.00, 10405306368.00)
    },
    {
        'name': '64',
        'base': (57843224576.00, 57828114432.00),
        'cksm': (24050266112.00, 22438096896.00),
        'uksm': (48851648512.00, 44084379648.00),
        'ksm' : (49472663552.00, 21119082496.00)
    },
    {
        'name': '128',
        'base': (113402871808.00, 113187479552.00),
        'cksm': (48313876480.00, 44245983232.00),
        'uksm': (90445701120.00, 85847764992.00),
        'ksm' : (96317542400.00, 42029580288.00)
    }
]

cksmPeakArr = []
uksmPeakArr = []
ksmPeakArr = []
tickArr = []

for dataDict in oriData:
    tickArr.append(dataDict['name'])
    curCKSM = dataDict['cksm'][0]
    curUKSM = dataDict['uksm'][0]
    curBase = dataDict['base'][0]
    curKSM = dataDict['ksm'][0]
    cksmPeakArr.append(float(curBase-curCKSM)/curBase*100)
    uksmPeakArr.append(float(curBase-curUKSM)/curBase*100)
    ksmPeakArr.append(float(curBase-curKSM)/curBase*100)

cksmStableArr = []
uksmStableArr = []
ksmStableArr = []

for dataDict in oriData:
    # tickArr.append(dataDict['name'])
    curCKSM = dataDict['cksm'][1]
    curUKSM = dataDict['uksm'][1]
    curBase = dataDict['base'][1]
    curKSM = dataDict['ksm'][1]
    cksmStableArr.append(float(curBase-curCKSM)/curBase*100)
    uksmStableArr.append(float(curBase-curUKSM)/curBase*100)
    ksmStableArr.append(float(curBase-curKSM)/curBase*100)

# print(cksmArr)
# print(tickArr)
print(cksmStableArr)
print(uksmStableArr)
print(ksmStableArr)
print(cksmPeakArr)
print(uksmPeakArr)
print(ksmPeakArr)

x=np.arange(len(tickArr))
width = 0.4

plt.figure(figsize=(9,6))

plt.plot(range(len(ksmStableArr)), ksmStableArr, color='tab:olive', label="KSM+_stable", linewidth=4, marker='^', markersize=9)
plt.plot(range(len(uksmStableArr)), uksmStableArr, color='tab:orange', label="UKSM_stable", linewidth=4, marker='s', markersize=9)
plt.plot(range(len(cksmStableArr)), cksmStableArr, color='tab:green', label="CKSM_stable", linewidth=4, marker='D', markersize=9)

plt.plot(range(len(ksmPeakArr)), ksmPeakArr, color='tab:olive', label="KSM+_peak", linestyle='--', linewidth=4, marker='^', markersize=9)
plt.plot(range(len(uksmPeakArr)), uksmPeakArr, color='tab:orange', label="UKSM_peak", linestyle='--', linewidth=4, marker='s', markersize=9)
plt.plot(range(len(cksmPeakArr)), cksmPeakArr, color='tab:green', label="CKSM_peak", linestyle='--', linewidth=4, marker='D', markersize=9)


plt.ylabel('Deduplication Rate(%)', fontsize=26)
plt.yticks(fontsize=20)
plt.ylim(0,100)

# xfmt = PercentFormatter(xmax=1, decimals=1)
# plt.gca().yaxis.set_major_formatter(xfmt)

plt.xticks(x,tickArr, fontsize=20)
plt.xlabel('Main Memory Capacity(GB)', fontsize=26)

plt.subplots_adjust(left=0.12, right=0.98, top=0.96, bottom=0.13)

plt.legend(fontsize=22, ncol=2, columnspacing=1, handlelength=3)

plt.savefig('scal_dedup_rate.pdf')
plt.show()