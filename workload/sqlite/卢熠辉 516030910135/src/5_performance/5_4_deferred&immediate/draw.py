import matplotlib.pyplot as plt

totalFile = 8

fileArr = []
for i in range(totalFile):
    fileArr.append(open('testData\\testData'+str(i), 'r'))

cur = 0
for i in range(totalFile):
    cur += int(fileArr[i].readline())
totalNum = int(cur/totalFile)

timeDeferred = []
timeImmediate = []
timeExclusive = []
operateNum = []

for i in range(totalNum):
    cur = 0.0
    for j in range(totalFile):
        cur += float(fileArr[j].readline())
    cur /= totalFile
    operateNum.append(cur)
for i in range(totalNum):
    cur = 0.0
    for j in range(totalFile):
        cur += float(fileArr[j].readline())
    cur /= totalFile
    timeDeferred.append(cur)
for i in range(totalNum):
    cur = 0.0
    for j in range(totalFile):
        cur += float(fileArr[j].readline())
    cur /= totalFile
    timeImmediate.append(cur)
for i in range(totalNum):
    cur = 0.0
    for j in range(totalFile):
        cur += float(fileArr[j].readline())
    cur /= totalFile
    timeExclusive.append(cur)

plt.title('5.4 deferred & immediate & exclusive')
plt.plot(operateNum, timeDeferred, color='red', label='DEFERRED')
plt.plot(operateNum, timeImmediate, color='blue', label='IMMEDIATE')
plt.plot(operateNum, timeExclusive, color='skyblue', label='EXCLUSIVE')
plt.legend()

plt.xlabel('scale')
plt.ylabel('time')
plt.show()
