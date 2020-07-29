import matplotlib.pyplot as plt

totalFile = 8

fileArr = []
for i in range(totalFile):
    fileArr.append(open('testData\\testData'+str(i), 'r'))

cur = 0
for i in range(totalFile):
    cur += int(fileArr[i].readline())
totalNum = int(cur/totalFile)

timeExeMany = []
timeOneCommit = []
timeMultiCommit = []
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
    timeExeMany.append(cur)
# for i in range(totalNum):
#     cur = 0.0
#     for j in range(totalFile):
#         cur += float(fileArr[j].readline())
#     cur /= totalFile
#     timeMultiCommit.append(cur)
for i in range(totalNum):
    cur = 0.0
    for j in range(totalFile):
        cur += float(fileArr[j].readline())
    cur /= totalFile
    timeOneCommit.append(cur)


mul = 0.0
for i in range(totalNum):
    mul += float(timeOneCommit[i])/timeExeMany[i]
mul /= totalNum
print(mul)

plt.title('5.3 execute & executemany')
plt.plot(operateNum, timeExeMany, color='red', label='executemany')
plt.plot(operateNum, timeOneCommit, color='blue', label='execute')
# plt.plot(operateNum, timeMultiCommit, color='skyblue', label='execute-commit')
plt.legend()

plt.xlabel('scale')
plt.ylabel('time')
plt.show()
