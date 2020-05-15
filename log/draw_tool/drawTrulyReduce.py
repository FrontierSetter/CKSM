import numpy as np
import matplotlib.pyplot as plt
 
X=[]
Y=[]

idx = 0.0

filePath = input('file: ')
startStamp = int(input('start: '))
stopStamp = int(input('stop: '))

curFile = open(filePath, 'r')

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

    if curTime > startStamp:
        X.append(idx)
        Y.append(cur_merged-base_merge)
        idx += 0.25
    else:
        base_merge = cur_merged
        base_notmerge = cur_notmerged

    if curTime > stopStamp:
        break


plt.figure()
plt.plot(X,Y)
plt.show()