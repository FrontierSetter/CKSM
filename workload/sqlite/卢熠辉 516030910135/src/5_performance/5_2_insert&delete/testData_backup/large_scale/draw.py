import matplotlib.pyplot as plt

totalFile = 1

fileArr = []
for i in range(totalFile):
    # fileArr.append(open('testData\\testData'+str(i), 'r'))
    
    # fileArr.append(open('testData_backup\\large_scale\\testData'+str(i), 'r'))
    fileArr.append(open('testData_backup\\large_scale\\testData'+str(i), 'r'))

cur = 0
for i in range(totalFile):
    cur += int(fileArr[i].readline())
totalNum = int(cur/totalFile)

timeInsert = []
timeDelete = []
timeDeleteMultiKey = []
# timeDeleteMultiNotKey = []
timeDeleteMultiKeyReverse = []
timeDeleteMultiKeyRandom = []
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
    timeInsert.append(cur)
for i in range(totalNum):
    cur = 0.0
    for j in range(totalFile):
        cur += float(fileArr[j].readline())
    cur /= totalFile
    timeDelete.append(cur)
for i in range(totalNum):
    cur = 0.0
    for j in range(totalFile):
        cur += float(fileArr[j].readline())
    cur /= totalFile
    timeDeleteMultiKey.append(cur)
# for i in range(totalNum):
#     cur = 0.0
#     for j in range(totalFile):
#         cur += float(fileArr[j].readline())
#     cur /= totalFile
#     timeDeleteMultiNotKey.append(cur)
for i in range(totalNum):
    cur = 0.0
    for j in range(totalFile):
        cur += float(fileArr[j].readline())
    cur /= totalFile
    timeDeleteMultiKeyReverse.append(cur)
for i in range(totalNum):
    cur = 0.0
    for j in range(totalFile):
        cur += float(fileArr[j].readline())
    cur /= totalFile
    timeDeleteMultiKeyRandom.append(cur)

plt.title('Insert & Delete')
# plt.plot(operateNum, timeInsert, color='red', label='Insert')
# plt.plot(operateNum, timeDelete, color='blue', label='Delete')
# plt.plot(operateNum, timeDeleteMultiKey, color='skyblue', label='DeleteMultiKey')
# plt.plot(operateNum, timeDeleteMultiNotKey, color='tan', label='DeleteMultiNotKey')
# plt.plot(operateNum, timeDeleteMultiKeyReverse, color='seagreen', label='DeleteMultiKeyReverse')
plt.plot(operateNum, timeDeleteMultiKeyRandom, color='violet', label='DeleteMultiKeyRandom')
plt.legend()

plt.xlabel('data scale')
plt.ylabel('time')
plt.show()
