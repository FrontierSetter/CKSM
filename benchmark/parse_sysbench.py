curName = input('which file: ')
batchNum = int(input('batchNum: '))

testName = ['mem_read_seq', 'mem_write_seq', 'mem_read_rnd', 'mem_write_rnd']

for test in testName:
    curTotal = 0.0
    for idx in range(batchNum):
        curFilePath = curName+'/'+test+'_'+str(idx)
        curFile = open(curFilePath, 'r')
        while True:
            curLine = curFile.readline()
            if curLine == '':
                break
            if 'transferred' in curLine:
                curNum = float(curLine.split(' ')[3].lstrip('('))
                # print(curNum)
                curTotal += curNum
                break
    print(test+':'+str(curTotal/batchNum))

