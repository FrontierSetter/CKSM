import numpy as np
import matplotlib.pyplot as plt

# 5
# kvm2.10nh-ksm100/test_data/cpu_usage.log
# 1578654573
# 332
# KSM-100
# kvm2.10nh-uksm-2/test_data/cpu_usage.log
# 1578650851
# 77
# UKSM
# kvm2.10nh-pksm50/test_data/cpu_usage.log
# 1578644443
# 336
# PKSM-50
# kvm2.10nh-pksm100/test_data/cpu_usage.log
# 1578643369
# 235
# PKSM-100
# kvm2.10nh-pksm200/test_data/cpu_usage.log
# 1578642578
# 195
# PKSM-200


# 2
# nginx64-uksm-2/test_data/cpu_usage.log
# 1578546453
# 100
# UKSM
# nginx64-pksm50/test_data/cpu_usage.log
# 1578541782
# 100
# CKSM-50

# 2
# nginx32-uksm-2/test_data/cpu_usage.log
# 1578469992
# 60
# UKSM
# nginx32-pksm100-1/test_data/cpu_usage.log
# 1578470749
# 60
# CKSM-50

# 2
# nginx16-uksm/test_data/cpu_usage.log
# 1578751011
# 30
# UKSM
# nginx16-pksm50-2/test_data/cpu_usage.log
# 1578743261
# 30
# CKSM-50

# 2
# nginx128-uksm/test_data/cpu_usage.log
# 1578749354
# 200
# UKSM
# nginx128-pksm50/test_data/cpu_usage.log
# 1578734303
# 300
# CKSM-50

# 2
# nginx256-uksm/test_data/cpu_usage.log
# 1578749910
# 450
# UKSM
# nginx256-pksm50/test_data/cpu_usage.log
# 1578804727
# 900
# CKSM-50

X=[]
Y=[]
startStamp = []
filePath = []
lineLabel = []
stopTime = []

colorTable = {'UKSM':'orange', 'Base':'royalblue', 'PKSM-50':'forestgreen', 'PKSM-100':'red', 'PKSM-200':'darkorchid', 'PKSM-500':'goldenrod', 'KSM-100':'yellow'}



lineNum = int(input('lineNum: '))
idxGap = 1

for i in range(lineNum):
    filePath.append(input('file: '))
    startStamp.append(int(input('start: ')))
    stopTime.append(int(input('stop: ')))
    lineLabel.append(input('label: '))
    Y.append([])
    X.append([])

for i in range(lineNum):
    print(i)
    curFile = open(filePath[i], 'r')

    idx = 0.0
    newFile = True

    while True:
        curLine = curFile.readline().strip('\n')
        if curLine == '':
            if newFile :
                continue
            else:
                break
        newFile = False
        
        curTime = int(curLine)
        curLineArr = [x for x in curFile.readline().strip('\n').split(' ') if x]
        # print(curLineArr)
        # print(curLineArr)
        curPercent = float(curLineArr[8])

        if curTime >= startStamp[i]:
            Y[i].append(curPercent)
            X[i].append(idx)
            idx += 1

        if idx > stopTime[i]:
            break

    curFile.close()

# idx = 0.0
# for i in range(len(Y[0])):
#     X.append(idx)
#     idx += idxGap

print(X)
print(Y)


plt.figure(figsize=(9,6))


# plt.figure()
for i in range(lineNum):
    curTotal = 0
    for cpuUsage in Y[i]:
        curTotal += cpuUsage
    print(lineLabel[i])
    print(float(curTotal)/len(Y[i]))

plt.legend()

# plt.set_size_inches(18.5, 10.5)

plt.xlabel('Time(s)')
plt.ylabel('CPU(% one core)')

# plt.show()