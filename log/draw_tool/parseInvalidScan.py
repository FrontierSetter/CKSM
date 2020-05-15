filePath = input('file: ')
curFile = open(filePath, 'r')

totalLog = 0
sumLog = 0
logDic = {}

# pre_totalLog = 132518

while True:
    curLine = curFile.readline()
    if curLine == '':
        break
    if 'uksm_vir_pages_scaned' not in curLine:
        continue
    totalLog += 1
    curArr = curLine.strip('\n').split(' ')
    curLog = int(curArr[-1])
    sumLog += curLog
    # print(curLog)
    if curLog in logDic:
        logDic[curLog] += 1
    else:
        logDic[curLog] = 1

print(logDic)
print(totalLog)
print(float(sumLog)/totalLog)

for k in logDic:
    logDic[k] = float(logDic[k])/totalLog
print(logDic)
