filePath = input('file: ')
curFile = open(filePath, 'r')

cmpSkipped = 0
cmpCalled = 0
totalCnt = 0
# totalBucket = 0
startStamp = -1

startHashStamp = -1

partialHashTime = 0
partialHashCnt = 0
memcmpTime = 0
memcmpCnt = 0
sameTime = 0
sameCnt = 0
calHashTime = 0
calHashCnt = 0

while True:
    curLine = curFile.readline()
    if curLine == '':
        break
    if ('PKSM' not in curLine):
        continue
    
    if 'skip:' in curLine:
        curLineArr = curLine.strip('\n').split(' ')
        # print(curLineArr)
        cmpSkipped += int(curLineArr[curLineArr.index('skip:')+1].strip(','))
        cmpCalled += int(curLineArr[curLineArr.index('valid:')+1].strip(','))
        totalCnt += 1
    elif 'cmp start' in curLine:
        if startStamp > 0:
            print('wrong')
            print(curLine)
            break;
        curLineArr = curLine.strip('\n').split(' ')

        curTimeStr = curLineArr[curLineArr.index('PKSM')-1].strip(']').split('.')
        curTime = int(curTimeStr[0])*1000000+int(curTimeStr[1])

        startStamp = curTime
    elif 'cmp end' in curLine:
        if startStamp < 0:
            print('wrong')
            print(curLine)
            break;

        if 'not_count' in curLine:
            startStamp = -1
        else:
            curLineArr = curLine.strip('\n').split(' ')
            curTimeStr = curLineArr[curLineArr.index('PKSM')-1].strip(']').split('.')
            curTime = int(curTimeStr[0])*1000000+int(curTimeStr[1])
            if 'partial_hash' in curLine:
                partialHashTime += (curTime-startStamp)
                partialHashCnt += 1
            elif 'same' in curLine:
                sameTime += (curTime-startStamp)
                sameCnt += 1
            else:
                memcmpTime += (curTime-startStamp)
                memcmpCnt += 1

            startStamp = -1 
    elif 'partial_hash start' in curLine:
        if startHashStamp > 0:
            print('wrong')
            print(curLine)
            break;
        curLineArr = curLine.strip('\n').split(' ')

        curTimeStr = curLineArr[curLineArr.index('PKSM')-1].strip(']').split('.')
        curTime = int(curTimeStr[0])*1000000+int(curTimeStr[1])

        startHashStamp = curTime
    elif 'partial_hash end' in curLine:
        if startHashStamp < 0:
            print('wrong')
            print(curLine)
            break;
        curLineArr = curLine.strip('\n').split(' ')

        curTimeStr = curLineArr[curLineArr.index('PKSM')-1].strip(']').split('.')
        curTime = int(curTimeStr[0])*1000000+int(curTimeStr[1])
        
        calHashTime += (curTime-startHashStamp)
        calHashCnt += 1
        startHashStamp = -1



# print('skiped: '+str(cmpSkipped))
# print('called: '+str(cmpCalled))
# print('ratio: '+str(float(cmpSkipped)/(float(cmpSkipped+cmpCalled))))
# print('load: '+str(float(cmpSkipped+cmpCalled)/(float(totalCnt))))

# print('memcmpTime: '+str(memcmpTime)+' memcmpCnt: '+str(memcmpCnt)+' memcmpAve: '+str(memcmpTime/memcmpCnt))
# print('partialTime: '+str(partialHashTime)+' partialCnt: '+str(partialHashCnt)+' partialAve: '+str(partialHashTime/partialHashCnt))
# print('totalAvg: '+str((memcmpTime+partialHashTime)/(memcmpCnt+partialHashCnt)))
# print('sameTime: '+str(sameTime)+' sameCnt: '+str(sameCnt)+' sameAve: '+str(sameTime/sameCnt))

print('calculateTime: '+str(calHashTime)+' calHashCnt: '+str(calHashCnt)+' calHashAvg: '+str(calHashTime/calHashCnt))
