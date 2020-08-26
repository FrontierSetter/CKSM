import sys, os

inputFilePath = sys.argv[1]
pathTuple = os.path.split(inputFilePath)
print(pathTuple)

inputFile = open(inputFilePath, 'r')
outputFile = open(os.path.join(pathTuple[0], 'out_'+pathTuple[1]), 'w')

while True:
    curLine = inputFile.readline()
    if curLine == '':
        break
    curTime = curLine.strip('\n').split(' ')[1]
    curZero = inputFile.readline().split(' ')[6].strip(',')
    outputFile.write('%s\nzero\t%s\n' % (curTime, curZero))
    inputFile.readline()
    while True:
        curLine = inputFile.readline()
        if curLine == '\n' or curLine == '':
            outputFile.write('\n')
            break
        curLineArr = curLine.strip('\n').split()
        print(curLineArr)
        outputFile.write('%s\t%s\n' % (curLineArr[0], curLineArr[-1]))