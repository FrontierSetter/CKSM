filePath = input('file: ')
curFile = open(filePath, 'r')

cmpSkipped = 0
cmpCalled = 0

while True:
    curLine = curFile.readline()
    if curLine == '':
        break
    if ('PKSM' not in curLine) or ('skip:' not in curLine):
        continue
    
    curLineArr = curLine.strip('\n').split(' ')
    cmpSkipped += int(curLineArr[curLineArr.index('skip:')+1])
    cmpCalled += int(curLineArr[curLineArr.index('valid:')+1])

print('skiped: '+str(cmpSkipped))
print('called: '+str(cmpCalled))
print('ratio: '+str(float(cmpSkipped)/(float(cmpSkipped+cmpCalled))))