import sys, os

inputFilePath = sys.argv[1]
pathTuple = os.path.split(inputFilePath)
print(pathTuple)

inputFile = open(inputFilePath, 'r')
outputFile = open(os.path.join(pathTuple[0], 'diff_'+pathTuple[1]), 'w')

diffDict = {}
preZero = 0

while True:
    curLine = inputFile.readline()
    if curLine == '':
        break
    curTime = curLine.strip('\n')
    curZero = int(inputFile.readline().split()[1])
    outputFile.write('%s\nzero\t%d\n' % (curTime, curZero-preZero))
    preZero = curZero
    inputFile.readline()
    while True:
        curLine = inputFile.readline()
        if curLine == '\n' or curLine == '':
            outputFile.write('\n')
            break
        curLineArr = curLine.strip('\n').split()
        
        curIdx = curLineArr[0]
        curCnt = int(curLineArr[1])

        if curIdx not in diffDict:
            diffDict[curIdx] = 0

        outputFile.write('%s\t%d\n' % (curIdx, curCnt-diffDict[curIdx]))

        diffDict[curIdx] = curCnt