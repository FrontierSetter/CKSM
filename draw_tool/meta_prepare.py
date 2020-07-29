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
outputFile = open(os.path.join(pathTuple[0], 'out_'+pathTuple[1]), 'w')


while True:
    curLine = inputFile.readline().strip('\n')
    if curLine == "":
        break

    curTime = int(curLine)
    curMeta = 0.0

    for i in range(3):
        inputFile.readline()
        curSize = int(inputFile.readline())
        curNum = int(inputFile.readline())
        curMeta = curSize*curNum
    

    outputFile.write("%d,%d\n" % (curTime, curMeta))

outputFile.close()
inputFile.close()