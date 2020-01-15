import numpy as np
import matplotlib.pyplot as plt

# ========================== fork ==============================

# fork_sharing.pdf
# 5
# 0.25
# 15
# KSM-fork-100/test_data/ksm_pages_sharing.log
# 1578291397
# KSM-50
# KSM-fork-200/test_data/ksm_pages_sharing.log
# 1578289179
# KSM-100
# UKSM-fork/bash/test_data/pages_sharing.log
# 1578060313
# UKSM
# PKSM-fork-100/bash/test_data/pksm_pages_sharing.log
# 1578133397
# CKSM-50
# PKSM-fork-200-2/bash/test_data/pksm_pages_sharing.log
# 1578132628
# CKSM-100


# 4
# 0.25
# 8
# UKSM-fork/bash/test_data/pages_sharing.log
# 1578060313
# UKSM
# UKSM-fork/bash/test_data/pages_sharing.log
# 1578060315
# UKSM
# PKSM-fork-200-2/bash/test_data/pksm_pages_sharing.log
# 1578132628
# CKSM-200
# PKSM-fork-500/test_data/pksm_pages_sharing.log
# 1578131114
# CKSM-500

# 2
# 0.25
# 8
# UKSM-fork-12-2/bash/test_data/pages_sharing.log
# 1578140021
# UKSM
# PKSM-fork-200-12/bash/test_data/pksm_pages_sharing.log
# 1578138951
# CKSM-200

# ==================== quick ================================

# quick_4_5.pdf
# 3
# 0.11
# 25
# quick-KSM-200-4096-4-5-ver/test_data/ksm_pages_sharing.log
# 1578294856
# KSM-50
# quick-UKSM-4096-4-5-2/test_data/pages_sharing.log
# 1578232326
# UKSM
# quick-PKSM-200-4096-4-5/test_data/pksm_pages_sharing.log
# 1578230743
# CKSM-50

# quick_2_5.pdf
# 3
# 0.11
# 13
# quick-KSM-200-4096-2-5-ver/test_data/ksm_pages_sharing.log
# 1578295849
# KSM-50
# quick-UKSM-4096-2-5/test_data/pages_sharing.log
# 1578233847
# UKSM
# quick-PKSM-200-4096-2-5/test_data/pksm_pages_sharing.log
# 1578234211
# CKSM-50

# quick_8_5.pdf
# 3
# 0.11
# 50
# quick-KSM-200-4096-8-5-ver/test_data/ksm_pages_sharing.log
# 1578296001
# KSM-50
# quick-UKSM-4096-8-5/test_data/pages_sharing.log
# 1578233613
# UKSM
# quick-PKSM-200-4096-8-5/test_data/pksm_pages_sharing.log
# 1578234399
# CKSM-50
 
X=[]
Y=[]
startStamp = []
filePath = []
lineLabel = []

colorTable = {'UKSM':'orange', 'Base':'royalblue', 'CKSM-50':'forestgreen', 'CKSM-100':'red', 'CKSM-200':'darkorchid', 'CKSM-500':'goldenrod', 'KSM-100':'violet', 'KSM-200':'chocolate', 'KSM-50':'rosybrown'}
markerTable = {'UKSM':'s', 'Base':'o', 'CKSM-50':'v', 'CKSM-100':'^', 'CKSM-200':'<', 'CKSM-500':'>', 'KSM-100':'x', 'KSM-200':'*', 'KSM-50':'D'}



figFileName = input('figFileName: ')
lineNum = int(input('lineNum: '))
idxGap = float(input('timeGap: '))
stopTime = int(input('stop: '))

for i in range(lineNum):
    filePath.append(input('file: '))
    startStamp.append(int(input('start: ')))
    lineLabel.append(input('label: '))
    Y.append([])

for i in range(lineNum):
    print(i)
    curFile = open(filePath[i], 'r')

    baseSharing = 0
    idx = 0.0

    while True:
        curLine = curFile.readline().strip('\n')
        if curLine == '':
            break
        
        curTime = int(curLine)
        curSharing = int(curFile.readline().strip('\n'))
        trueSharing = curSharing - baseSharing

        if curTime >= startStamp[i]:
            Y[i].append(trueSharing)
            idx += idxGap
        else:
            baseSharing = curSharing

        if idx >= stopTime:
            break

    curFile.close()

idx = 0.0
for i in range(len(Y[0])):
    X.append(idx)
    idx += idxGap

print(X)
print(Y)


plt.figure(figsize=(9,6))


# plt.figure()
for i in range(lineNum):
    plt.plot(X,Y[i], label=lineLabel[i], linewidth=4, marker=markerTable[lineLabel[i]], color=colorTable[lineLabel[i]], markevery=10, markersize=8)
    # plt.plot(X,Y[i], label=lineLabel[i], linewidth=4, marker='o')

plt.legend(fontsize=14)

# plt.set_size_inches(18.5, 10.5)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Time(s)', fontsize=16)
plt.ylabel('Virtual Pages Released', fontsize=16)

plt.subplots_adjust(left=0.12, right=0.98, top=0.98, bottom=0.09)

plt.savefig(figFileName)

plt.show()