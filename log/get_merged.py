curFile = open('uksm_pages_map_cnt.log', 'r')
outFile = open('uksm_pages_merged.log', 'w')

base_merge = 0
base_notmerge = 0

while True:
    curLine = curFile.readline().strip('\n')
    if curLine == '':
        break
    
    curTime = int(curLine)
    curFile.readline()
    cur_merged = int(curFile.readline())
    cur_notmerged = int(curFile.readline())

    outFile.write(str(curTime)+'\n')
    outFile.write(str(cur_merged)+'\n')

    