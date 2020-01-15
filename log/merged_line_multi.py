import numpy as np
import matplotlib.pyplot as plt

# fork_merged.pdf
# 7
# KSM-fork-100/test_data/ksm_pages_merged.log
# 1578291397
# KSM-100
# KSM-fork-200/test_data/ksm_pages_merged.log
# 1578289179
# KSM-200
# KSM-fork-500/test_data/ksm_pages_merged.log
# 1578290210
# KSM-500
# UKSM-fork/bash/test_data/uksm_pages_merged.log
# 1578060313
# UKSM
# PKSM-fork-100/bash/test_data/pksm_pages_merged.log
# 1578133397
# CKSM-100
# PKSM-fork-200-2/bash/test_data/pksm_pages_merged.log
# 1578132628
# CKSM-200
# PKSM-fork-500/test_data/pksm_pages_merged.log
# 1578131114
# CKSM-500

# fork_merged.pdf
# 5
# KSM-fork-100/test_data/ksm_pages_merged.log
# 1578291397
# KSM-50
# KSM-fork-200/test_data/ksm_pages_merged.log
# 1578289179
# KSM-100
# UKSM-fork/bash/test_data/uksm_pages_merged.log
# 1578060313
# UKSM
# PKSM-fork-100/bash/test_data/pksm_pages_merged.log
# 1578133397
# CKSM-50
# PKSM-fork-200-2/bash/test_data/pksm_pages_merged.log
# 1578132628
# CKSM-100

# UKSM-fork/bash/test_data/uksm_pages_merged.log
# 1578060315
# UKSM-moved

# fork_merged_lite.pdf
# 3
# KSM-fork-200/test_data/ksm_pages_merged.log
# 1578289183
# KSM-200-moved
# UKSM-fork/bash/test_data/uksm_pages_merged.log
# 1578060315
# UKSM-moved
# PKSM-fork-200-2/bash/test_data/pksm_pages_merged.log
# 1578132628
# CKSM-200



# 2
# UKSM-fork-12/bash/test_data/uksm_pages_merged.log
# 1578139229
# UKSM
# PKSM-fork-200-12/bash/test_data/pksm_pages_merged.log
# 1578138951
# PKSM-200

# 2
# UKSM-fork-12-2/bash/test_data/uksm_pages_merged.log
# 1578140017
# UKSM
# PKSM-fork-200-12/bash/test_data/pksm_pages_merged.log
# 1578138951
# PKSM-200
 
X=[]
Y=[]
startStamp = []
filePath = []
lineLabel = []

colorTable = {'UKSM':'orange', 'Base':'royalblue', 'CKSM-50':'forestgreen', 'CKSM-100':'red', 'CKSM-200':'darkorchid', 'CKSM-500':'goldenrod', 'KSM-100':'violet', 'KSM-200':'chocolate', 'KSM-50':'rosybrown'}
markerTable = {'UKSM':'s', 'Base':'o', 'CKSM-50':'v', 'CKSM-100':'^', 'CKSM-200':'<', 'CKSM-500':'>', 'KSM-100':'x', 'KSM-200':'*', 'KSM-50':'D'}



figFileName = input('figFileName: ')


lineNum = int(input('lineNum: '))

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
            idx += 0.25
        else:
            baseSharing = curSharing

        if idx >= 12.0:
            break

    curFile.close()

plt.figure(figsize=(9,6))

idx = 0.0
for i in range(len(Y[0])):
    X.append(idx)
    idx += 0.25

print(X)
print(Y)

# plt.figure()
for i in range(lineNum):
    plt.plot(X,Y[i], label=lineLabel[i], linewidth=4, marker=markerTable[lineLabel[i]], color=colorTable[lineLabel[i]], markevery=5, markersize=8)

plt.legend(fontsize=14)

# plt.set_size_inches(18.5, 10.5)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.xlabel('Time(s)', fontsize=16)
plt.ylabel('Physical Pages Released', fontsize=16)


plt.subplots_adjust(left=0.11, right=0.98, top=0.98, bottom=0.09)

plt.savefig(figFileName)

plt.show()