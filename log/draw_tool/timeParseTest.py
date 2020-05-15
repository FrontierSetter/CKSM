filePath = input('file: ')
curFile = open(filePath, 'r')

while True:
    curLine = curFile.readline()
    if curLine == '':
        break
    if ('PKSM' not in curLine):
        continue

    curLineArr = curLine.strip('\n').split(' ')

    curTimeStr = curLineArr[curLineArr.index('PKSM')-1].strip(']').split('.')
    curTime = int(curTimeStr[0])*1000000+int(curTimeStr[1])

    print(curTime)