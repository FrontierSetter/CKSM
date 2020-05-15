filePath = input('file: ')
curFile = open(filePath, 'r')

shouldRun = False

fileLine = 0

processPageCnt = 0
processPageDic = {}

while True:
    fileLine += 1
    curLine = curFile.readline()
    if curLine == '':
        break
    if 'PKSM' not in curLine:
        continue
    if ('run_store evoked' in curLine):
        print(curLine)
        # if curLine[16] == '1':
        shouldRun = True
    if not shouldRun:
        continue
    if 'pksm_do_scan : get page' in curLine:
        curLineArr = curLine.strip('\n').split(' ')
        curPage = curLineArr[17]
        # print(curPage)
        if(curPage in processPageDic):
            processPageDic[curPage] += 1
        else:
            processPageDic[curPage] = 1

print(processPageDic)
print('pageProcessed: ',len(processPageDic))
print('fileLine: ', fileLine)
        