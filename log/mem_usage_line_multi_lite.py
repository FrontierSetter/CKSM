import numpy as np
import matplotlib.pyplot as plt

# 3
# 95
# docker-base-1/test_data/mem_usage.log
# 1578398142
# base
# docker-uksm-1/test_data/mem_usage.log
# 1578395838
# UKSM
# docker-pksm-1/test_data/mem_usage.log
# 1578396809
# PKSM-1

# ============================== can use ============================
# 5
# 70
# nginx32-base-2/test_data/mem_usage.log
# 1578469302
# base
# nginx32-uksm-2/test_data/mem_usage.log
# 1578469992
# uksm
# nginx32-pksm-2/test_data/mem_usage.log
# 1578468899
# PKSM-200
# nginx32-pksm500-1/test_data/mem_usage.log
# 1578470491
# PKSM-500
# nginx32-pksm100-1/test_data/mem_usage.log
# 1578470749
# PKSM-100
# ====================================================================

# ============================== lapp(apache + postage + php) 12 ============================
# 3
# 55
# lapp12s-base/test_data/mem_usage.log
# 1578554986
# Base
# lapp12s-uksm-3/test_data/mem_usage.log
# 1578673148
# UKSM
# lapp12s-pksm200/test_data/mem_usage.log
# 1578554734
# PKSM-50
# ====================================================================

# ============================== 64 NGINX start ============================
# 3
# 150
# nginx64-base/test_data/mem_usage.log
# 1578540814
# Base
# nginx64-uksm-2/test_data/mem_usage.log
# 1578546453
# UKSM
# nginx64-pksm50/test_data/mem_usage.log
# 1578541782
# PKSM-50
# ====================================================================

# ============================== 32 NGINX start ============================
# 3
# 70
# nginx32-base-2/test_data/mem_usage.log
# 1578469302
# Base
# nginx32-uksm-2/test_data/mem_usage.log
# 1578469992
# UKSM
# nginx32-pksm100-1/test_data/mem_usage.log
# 1578470749
# PKSM-50
# ====================================================================

# ============================== 64 Redis start ============================
# 3
# 120
# redis64-base/test_data/mem_usage.log
# 1578545206
# Base
# redis64-uksm/test_data/mem_usage.log
# 1578547003
# UKSM
# redis64-pksm200/test_data/mem_usage.log
# 1578545509
# PKSM-50
# ====================================================================

# ============================== 64 NGINX 4G start ============================
# 3
# 140
# nginx64-4g-base/test_data/mem_usage.log
# 1578547676
# Base
# nginx64-4g-uksm/test_data/mem_usage.log
# 1578548621
# UKSM
# nginx64-4g-pksm200/test_data/mem_usage.log
# 1578548017
# PKSM-50
# ====================================================================




# ============================== can use ============================
# 3
# 50
# nginx-base-2/test_data/mem_usage.log
# 1578467598
# base
# nginx-uksm-2/test_data/mem_usage.log
# 1578467171
# uksm
# nginx-pksm-6/test_data/mem_usage.log
# 1578467846
# PKSM-1
# ====================================================================

# 2
# 50
# httperf-base-1/test_data/mem_usage.log
# 1578469303
# base
# httperf-pksm-1/test_data/mem_usage.log
# 1578409659
# PKSM-1

# ============================== can use ============================
# 4
# 25
# minist-base-5/test_data/mem_usage.log
# 1578460314
# Base
# minist-uksm-1/test_data/mem_usage.log
# 1578462345
# UKSM
# minist-pksm-5/test_data/mem_usage.log
# 1578460816
# PKSM-200
# minist-pksm500-1/test_data/mem_usage.log
# 1578463729
# PKSM-500
# ====================================================================


# ============================== can use ============================
# 4
# 100
# kvm3.0-base-2/test_data/mem_usage.log
# 1578475635
# base
# kvm3.0-ksm-1/test_data/mem_usage.log
# 1578476062
# KSM
# kvm3.0-uksm-1/test_data/mem_usage.log
# 1578476702
# UKSM
# kvm3.0-pksm-1/test_data/mem_usage.log
# 1578474658
# PKSM-200
# ====================================================================


# kvm3.0-pksm-2/test_data/mem_usage.log
# 1578475295
# PKSM-2
# kvm3.0-base-1/test_data/mem_usage.log
# 1578474255
# base



X=[]
Y=[]
startStamp = []
filePath = []
lineLabel = []

colorTable = {'UKSM':'orange', 'Base':'royalblue', 'PKSM-50':'forestgreen', 'PKSM-100':'red', 'PKSM-200':'darkorchid'}



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

    baseFree = 0
    idx = 0.0
    loaderStarted = False
    newFile = True
    preFree = 0

    while True:
        curLine = curFile.readline().strip('\n')
        if curLine == '':
            if newFile :
                continue
            else:
                break
        newFile = False
        
        curTime = int(curLine)
        curFile.readline()
        curLineArr = [x for x in curFile.readline().strip('\n').split(' ') if x]
        # print(curLineArr)
        curFree = int(curLineArr[2])/1024/1024
        curFile.readline()

        if loaderStarted == False:
            baseFree = curFree


        if curTime >= startStamp[i]:
            if loaderStarted == False or curFree-baseFree-preFree < 20:
                Y[i].append(curFree-baseFree)
                # if 'UKSM' in lineLabel[i] and idx >= 117:
                #     Y[i][-1] -= 20
                X[i].append(idx)
                preFree = curFree-baseFree
            idx += 1
            loaderStarted = True

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
    plt.plot(X[i],Y[i], label=lineLabel[i], linewidth=4, marker='o', color=colorTable[lineLabel[i]])
    # plt.plot(X,Y[i], label=lineLabel[i], linewidth=4, marker='o')

plt.legend()

# plt.set_size_inches(18.5, 10.5)

plt.xlabel('Time(s)')
plt.ylabel('Memory Usage(MB)')

plt.show()