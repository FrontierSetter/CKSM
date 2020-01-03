import numpy as np
import matplotlib.pyplot as plt
 
X=[]
Y=[]

idx = 0.0

filePath = input('file: ')
startStamp = int(input('start: '))
stopStamp = int(input('stop: '))

curFile = open(filePath, 'r')

baseSharing = 0

while True:
    curLine = curFile.readline().strip('\n')
    if curLine == '':
        break
    
    curTime = int(curLine)
    curSharing = int(curFile.readline().strip('\n'))
    trueSharing = curSharing - baseSharing

    if curTime > startStamp:
        X.append(idx)
        Y.append(trueSharing)
        idx += 0.25
    else:
        baseSharing = curSharing

    if curTime > stopStamp:
        break


plt.figure()
plt.plot(X,Y)
plt.show()