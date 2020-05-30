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
    curLineArr = [x for x in inputFile.readline().strip('\n').split(' ') if x]
    
    if len(curLineArr) < 8:
        continue
    
    curMem = float(curLineArr[8])

    outputFile.write("%d,%f\n" % (curTime, curMem))

outputFile.close()
inputFile.close()