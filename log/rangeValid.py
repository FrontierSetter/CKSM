totalNum = 65003720.0

filePath = input('file: ')
curFile = open(filePath, 'r')
writeFile = open('rangeAna.log', 'w')
pos = 0

totalRange = 0.0

while True:
    curLine = curFile.readline().strip('\n')
    if curLine == '':
        break
    curNum = int(curLine)
    if curNum == 0:
        pos += 1
        continue
    curRange = curNum / totalNum
    totalRange += curRange
    print(str(pos)+': '+str(curRange)+', '+str(totalRange))
    writeFile.write(str(pos)+': '+str(curRange)+', '+str(totalRange)+'\n')
    pos += 1

