import numpy as np
import matplotlib.pyplot as plt

# 3
# UKSM-fork/bash/test_data/pages_sharing.log
# 1578060313
# UKSM
# PKSM-fork-200-2/bash/test_data/pksm_pages_sharing.log
# 1578132628
# PKSM-200
# PKSM-fork-500/test_data/pksm_pages_sharing.log
# 1578131114
# PKSM-500

# 4
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
# UKSM-fork-12-2/bash/test_data/pages_sharing.log
# 1578140021
# UKSM
# PKSM-fork-200-12/bash/test_data/pksm_pages_sharing.log
# 1578138951
# PKSM-200
 
X=[]
Y=[]
startStamp = []
filePath = []
lineLabel = []


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

        if idx >= 8.0:
            break

    curFile.close()

idx = 0.0
for i in range(len(Y[0])):
    X.append(idx)
    idx += 0.25

print(X)
print(Y)

# plt.figure()
for i in range(lineNum):
    plt.plot(X,Y[i], label=lineLabel[i], linewidth=4, marker='o')

plt.legend()

plt.xlabel('Time(s)')
plt.ylabel('pages sharing')

plt.show()