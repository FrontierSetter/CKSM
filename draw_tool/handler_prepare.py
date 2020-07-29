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
outputFileExit = open(os.path.join(pathTuple[0], 'out_exit_'+pathTuple[1]), 'w')
outputFileAdd = open(os.path.join(pathTuple[0], 'out_add_'+pathTuple[1]), 'w')

inputFile.readline()

while True:
    curLine = inputFile.readline().strip('\n')
    if curLine == "":
        break

    curTime = int(curLine.strip('\n').split()[-1])

    exitLineArr = inputFile.readline().strip('\n').split()
    exitTime = float(exitLineArr[3].strip(','))
    exitCnt = float(exitLineArr[6].strip(','))
    outputFileExit.write("%d,%f,%d\n" % (curTime, exitTime/exitCnt, exitCnt))
    
    addLineArr = inputFile.readline().strip('\n').split()
    addTime = float(addLineArr[3].strip(','))
    addCnt = float(addLineArr[6].strip(','))
    outputFileAdd.write("%d,%f,%d\n" % (curTime, addTime/addCnt, addCnt))

    inputFile.readline()
    inputFile.readline()
    
outputFileExit.close()
outputFileAdd.close()
inputFile.close()