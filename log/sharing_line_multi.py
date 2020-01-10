import numpy as np
import matplotlib.pyplot as plt

# ========================== fork ==============================

# 7
# 0.25
# 15
# KSM-fork-100/test_data/ksm_pages_sharing.log
# 1578291397
# KSM-100
# KSM-fork-200/test_data/ksm_pages_sharing.log
# 1578289179
# KSM-200
# KSM-fork-500/test_data/ksm_pages_sharing.log
# 1578290210
# KSM-500
# UKSM-fork/bash/test_data/pages_sharing.log
# 1578060313
# UKSM
# PKSM-fork-100/bash/test_data/pksm_pages_sharing.log
# 1578133397
# PKSM-100
# PKSM-fork-200-2/bash/test_data/pksm_pages_sharing.log
# 1578132628
# PKSM-200
# PKSM-fork-500/test_data/pksm_pages_sharing.log
# 1578131114
# PKSM-500

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
# PKSM-200
# PKSM-fork-500/test_data/pksm_pages_sharing.log
# 1578131114
# PKSM-500

# 2
# 0.25
# 8
# UKSM-fork-12-2/bash/test_data/pages_sharing.log
# 1578140021
# UKSM
# PKSM-fork-200-12/bash/test_data/pksm_pages_sharing.log
# 1578138951
# PKSM-200

# ==================== quick ================================

# 3
# 0.11
# 25
# quick-KSM-200-4096-4-5-ver/test_data/ksm_pages_sharing.log
# 1578294856
# KSM-200
# quick-UKSM-4096-4-5-2/test_data/pages_sharing.log
# 1578232326
# UKSM
# quick-PKSM-200-4096-4-5/test_data/pksm_pages_sharing.log
# 1578230743
# PKSM-200

# 3
# 0.11
# 13
# quick-KSM-200-4096-2-5-ver/test_data/ksm_pages_sharing.log
# 1578295849
# KSM-200
# quick-UKSM-4096-2-5/test_data/pages_sharing.log
# 1578233847
# UKSM
# quick-PKSM-200-4096-2-5/test_data/pksm_pages_sharing.log
# 1578234211
# PKSM-200

# 3
# 0.11
# 50
# quick-KSM-200-4096-8-5-ver/test_data/ksm_pages_sharing.log
# 1578296001
# KSM-200
# quick-UKSM-4096-8-5/test_data/pages_sharing.log
# 1578233613
# UKSM
# quick-PKSM-200-4096-8-5/test_data/pksm_pages_sharing.log
# 1578234399
# PKSM-200
 
X=[]
Y=[]
startStamp = []
filePath = []
lineLabel = []


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
    plt.plot(X,Y[i], label=lineLabel[i], linewidth=4)
    # plt.plot(X,Y[i], label=lineLabel[i], linewidth=4, marker='o')

plt.legend()

# plt.set_size_inches(18.5, 10.5)

plt.xlabel('Time(s)')
plt.ylabel('pages sharing')

plt.show()