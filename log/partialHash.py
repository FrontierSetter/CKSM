filePath = input('file: ')
curFile = open(filePath, 'r')

diffPos = [0] * 4097
# print(diffPos)
totalCnt = 0
totalLine = 0

while True:
    curLine = curFile.readline()
    if curLine == '':
        break
    totalLine += 1
    # if totalLine%1000 == 0:
    #     print(totalLine)
    if ('memcmp_mine' in curLine):
        curLineArr = curLine.split(' ')
        # print(curLineArr[15].strip(','))
        try:
            tem = int(curLineArr[curLineArr.index('at')+1].strip(','))
        except:
            print(totalLine)
            print(curLineArr)
            print(curLineArr[curLineArr.index('at')+1].strip(','))
        else:
            # if tem >= 4097:
            # print(tem)
            diffPos[tem] += 1
            totalCnt += 1

print(diffPos)
print(totalCnt)

writeFile = open('partialHash.log', 'w')
for i in diffPos:
    writeFile.write(str(i)+'\n')
        
        