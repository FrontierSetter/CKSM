import numpy as np
import matplotlib.pyplot as plt

# ============================== can use ============================
# 4
# 70
# nginx32-uksm-2/test_data/cpu_usage.log
# 1578469992
# uksm
# nginx32-pksm-2/test_data/cpu_usage.log
# 1578468899
# CKSM-200
# nginx32-pksm500-1/test_data/cpu_usage.log
# 1578470491
# CKSM-500
# nginx32-pksm100-1/test_data/cpu_usage.log
# 1578470749
# CKSM-100
# ====================================================================

# ============================== 64 NGINX start ============================
# nginx_64_cpu.pdf
# 2
# 150
# nginx64-uksm-2/test_data/cpu_usage.log
# 1578546453
# UKSM
# nginx64-pksm50/test_data/cpu_usage.log
# 1578541782
# CKSM-50
# ====================================================================



# ============================== can use ============================
# 3
# 50
# nginx-base-2/test_data/cpu_usage.log
# 1578467598
# base
# nginx-uksm-2/test_data/cpu_usage.log
# 1578467171
# uksm
# nginx-pksm-6/test_data/cpu_usage.log
# 1578467846
# CKSM-1
# ====================================================================

# 2
# 50
# httperf-base-1/test_data/cpu_usage.log
# 1578469303
# base
# httperf-pksm-1/test_data/cpu_usage.log
# 1578409659
# CKSM-1

# ============================== can use ============================
# minist_cpu.pdf
# 3
# 30
# minist-uksm-1/test_data/cpu_usage.log
# 1578462345
# UKSM
# minist-pksm-5/test_data/cpu_usage.log
# 1578460816
# CKSM-200
# minist-pksm500-1/test_data/cpu_usage.log
# 1578463729
# CKSM-500
# ====================================================================


# ============================== can use ============================
# 3
# 100
# kvm3.0-ksm-1/test_data/cpu_usage.log
# 1578476062
# KSM
# kvm3.0-uksm-1/test_data/cpu_usage.log
# 1578476702
# UKSM
# kvm3.0-pksm-1/test_data/cpu_usage.log
# 1578474658
# CKSM-200
# ====================================================================


# kvm3.0-pksm-2/test_data/cpu_usage.log
# 1578475295
# CKSM-2
# kvm3.0-base-1/test_data/cpu_usage.log
# 1578474255
# base

# 4
# 70
# nginx32-pksm50/test_data/cpu_usage.log
# 1578543031
# CKSM-50
# nginx32-pksm100-1/test_data/cpu_usage.log
# 1578470749
# CKSM-100
# nginx32-pksm-2/test_data/cpu_usage.log
# 1578468899
# CKSM-200
# nginx32-pksm500-1/test_data/cpu_usage.log
# 1578470491
# CKSM-500

# 2
# 250
# kvm2.5nh-pksm100/test_data/cpu_usage.log
# 1578643369
# CKSM-100
# kvm2.5nh-pksm200/test_data/cpu_usage.log
# 1578642578
# CKSM-200

# 5
# 350
# kvm2.10nh-ksm100/test_data/cpu_usage.log
# 1578654573
# KSM-100
# kvm2.10nh-uksm-2/test_data/cpu_usage.log
# 1578650851
# UKSM
# kvm2.10nh-pksm50/test_data/cpu_usage.log
# 1578644443
# CKSM-50
# kvm2.10nh-pksm100/test_data/cpu_usage.log
# 1578643369
# CKSM-100
# kvm2.10nh-pksm200/test_data/cpu_usage.log
# 1578642578
# CKSM-200



X=[]
Y=[]
startStamp = []
filePath = []
lineLabel = []

colorTable = {'UKSM':'orange', 'Base':'royalblue', 'CKSM-50':'forestgreen', 'CKSM-100':'red', 'CKSM-200':'darkorchid', 'CKSM-500':'goldenrod', 'KSM-100':'yellow'}

figFileName = input('figFileName: ')


lineNum = int(input('lineNum: '))
idxGap = 1
stopTime = int(input('stop: '))

for i in range(lineNum):
    filePath.append(input('file: '))
    startStamp.append(int(input('start: ')))
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

        if idx > stopTime:
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
    # plt.scatter(X[i],Y[i], label=lineLabel[i],marker='o', c='',edgecolors=colorTable[lineLabel[i]])
    plt.plot(X[i],Y[i], label=lineLabel[i], linewidth=2, color=colorTable[lineLabel[i]])
    # plt.plot(X,Y[i], label=lineLabel[i], linewidth=4, marker='o')

plt.legend()

# plt.set_size_inches(18.5, 10.5)

plt.xlabel('Time(s)')
plt.ylabel('CPU(% one core)')


plt.subplots_adjust(left=0.09, right=0.98, top=0.98, bottom=0.09)

plt.savefig(figFileName)

plt.show()