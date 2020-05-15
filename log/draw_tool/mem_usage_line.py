import numpy as np
import matplotlib.pyplot as plt
 
X=[]
Y=[]

idx = 0.0

filePath = input('file: ')
startStamp = int(input('start: '))
stopStamp = int(input('stop: '))
timeGap = float(input('gap: '))

curFile = open(filePath, 'r')

baseFree = 0

while True:
    curLine = curFile.readline().strip('\n')
    if curLine == '':
        break
    
    curTime = int(curLine)
    curFile.readline()
    curLineArr = [x for x in curFile.readline().strip('\n').split(' ') if x]
    # print(curLineArr)
    curFree = int(curLineArr[4])/1024/1024
    curFile.readline()

    if curTime >= startStamp:
        X.append(idx)
        Y.append(curFree)
        idx += timeGap
    else:
        baseFree = curFree

    if curTime > stopStamp:
        break

print(X)
print(Y)

plt.figure()
plt.plot(X,Y)
plt.show()