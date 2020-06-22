import sys

outFile = open('lock_usage.log', 'w')

cpuNum = 8

fileLine = 0

timeBase = 0.0
preLog = (0,0,0)

for i in range(1, len(sys.argv)):
    filePath = sys.argv[i]
    print(filePath)
    curFile = open(filePath, 'r')

    while True:
        fileLine += 1
        curLine = curFile.readline()
        if curLine == '':
            break
        if 'PKSM' not in curLine:
            continue
        if 'lock' not in curLine:
            continue
        curArr = curLine.strip('\n').split()
        baseIdx = curArr.index('PKSM')
        curCPU = int(curArr[baseIdx+4])
        curAction = curArr[baseIdx+5]
        curTime = float(curArr[baseIdx-1].strip(']'))
        curFrom = curArr[baseIdx+2]

        if (curTime < timeBase) or (curTime == timeBase and preLog == (curCPU, curFile, curAction)):
            continue
        preLog = (curCPU, curFile, curAction)

        outFile.write("%f\t%d\t%s\t%s\n" % (curTime, curCPU, curAction, curFrom))

    curFile.close()
    
