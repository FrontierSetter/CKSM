import matplotlib.pyplot as plt

totalFile = 10

fileArr = []
for i in range(totalFile):
    fileArr.append(open('testData\\testData'+str(i), 'r'))

cur = 0
for i in range(totalFile):
    cur += int(fileArr[i].readline())
totalNum = int(cur/totalFile)

timeMemory = []
timeFile = []
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
    timeMemory.append(cur)
for i in range(totalNum):
    cur = 0.0
    for j in range(totalFile):
        cur += float(fileArr[j].readline())
    cur /= totalFile
    timeFile.append(cur)

# plt.figure(figsize=(12, 8)) 
plt.title('File & Memory (single commit)')
plt.plot(operateNum, timeMemory, color='red', label='Memory')
plt.plot(operateNum, timeFile, color='blue', label='File')
plt.legend()



plt.xlabel('insert scale')
plt.ylabel('time')
plt.show()
