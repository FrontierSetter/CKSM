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

preNormalArr = [0, 0, 0, 0, 0]
prePervageArr = [0, 0, 0, 0, 0, 0]

while True:
    curLine = inputFile.readline().strip('\n')
    if curLine == "":
        break

    curTime = int(curLine)
    outputFile.write("%d\n" % (curTime))

    curLineNormalArr = [int(x) for x in inputFile.readline().strip('\n').split(' ') if x]

    for i in range(5):
        outputFile.write("%d " % (curLineNormalArr[i]-preNormalArr[i]))
        preNormalArr[i] = curLineNormalArr[i]
    outputFile.write("\n")

    curLinePervageArr = [int(x) for x in inputFile.readline().strip('\n').split(' ') if x]

    for i in range(6):
        outputFile.write("%d " % (curLinePervageArr[i]-prePervageArr[i]))
        prePervageArr[i] = curLinePervageArr[i]
    outputFile.write("\n")

outputFile.close()
inputFile.close()