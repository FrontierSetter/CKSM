import numpy as np
import matplotlib.pyplot as plt

# UKSM-fork/bash/test_data/uksm_pages_map_cnt.log
# 1578060313

# UKSM-fork-12/bash/test_data/uksm_pages_map_cnt.log
# 1578139229

filePath = input('file: ')
startStamp = int(input('start: '))

curFile = open(filePath, 'r')

pre_merged = 0
pre_notmerged = 0
cur_merged = 0
cur_notmerged = 0

x_data = []
truly_merged = []
not_merged = []

idx = 0

while True:
    curLine = curFile.readline().strip('\n')
    if curLine == '':
        break
    
    curTime = int(curLine)

    curFile.readline()
    cur_merged = int(curFile.readline())
    cur_notmerged = int(curFile.readline())

    if curTime >= startStamp:
        truly_merged.append(cur_merged-pre_merged)
        not_merged.append(cur_notmerged-pre_notmerged)
        x_data.append(idx)
        idx += 0.25

    pre_merged = cur_merged
    pre_notmerged = cur_notmerged

    if idx >= 10.0:
        break


print(len(truly_merged))
print(idx)
plt.figure(figsize=(9,6))


plt.stackplot(x_data, truly_merged, not_merged, labels=['True merge', 'Fake merge'], colors=['coral', 'slategray'])
plt.legend(fontsize=16)

# plt.set_size_inches(18.5, 10.5)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.xlabel('Time(s)', fontsize=18)
plt.ylabel('Number of Pages Merged', fontsize=18)
plt.subplots_adjust(left=0.12, right=0.98, top=0.98, bottom=0.09)
plt.savefig('fake_merge.pdf')

plt.show()