import sys
import os.path

# 输出两列数据，用逗号分隔：时间戳，当时内存使用情况Byte
# 第一行为数据备注
# 第二行为基本参数：起始时间戳，内存基准
# 第一二行的信息需要人工填写

inputFilePath = sys.argv[1]
pathTuple = os.path.split(inputFilePath)
print(pathTuple)

inputFile = open(inputFilePath, 'r')
# outputFile = open(os.path.join(pathTuple[0], 'out_'+pathTuple[1]), 'w')

inputFile.readline()

maxMem = 0
stableMem = 0

baseArr = inputFile.readline().strip('\n').split(',')
baseTime = int(baseArr[0])
baseMem = float(baseArr[1])
compTime = int(baseArr[2])
# print(baseMem)

getBase = False

while True:
    curLine = inputFile.readline().strip('\n')
    if curLine == "":
        break

    curLineArr = curLine.strip('\n').split(',')
    curTime = int(curLineArr[0])
    curMem = int(curLineArr[1])
    # print("cur:%d base:%d out:%d" % (curMem, baseMem, curMem-baseMem))


    # outputFile.write("%d,%d\n" % (curTime, curMem))

    if curTime < baseTime:
        continue

    if not getBase:
        baseMem = curMem
        getBase = True
    
    curMem -= baseMem

    if curMem > maxMem:
        maxMem = curMem
    
    stableMem = curMem

inputFile.close()

print("max: %d\tstable: %d" % (maxMem, stableMem))