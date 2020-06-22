import sys
import matplotlib.pyplot as plt

curFile = open('lock_usage.log', 'r')

cpuNum = 8
fileLine = 0

cpuTry = [0.0]*cpuNum
cpuAcquire = [0.0]*cpuNum
cpuUnlock = [0.0]*cpuNum
cpuState = ['unlock']*cpuNum


while True:
    fileLine += 1
    curLine = curFile.readline().strip('\n')
    if curLine == '':
        break
    
    curArr = curLine.strip('\n').split()

    curTime = float(curArr[0])
    curCpu = int(curArr[1])
    curAction = curArr[2]

    if curAction == 'try':
        if cpuState[curCpu] != 'unlock':
            print('try before unlock at line %d' % (fileLine))
            print('|->cur:\t%s' % (curLine))
            print('|->sta: %s\ttry: %f\tacq: %f\tunlock: %f' % (cpuState[curCpu], cpuTry[curCpu], cpuAcquire[curCpu], cpuUnlock[curCpu]))
        cpuState[curCpu] = curAction
        cpuTry[curCpu] = curTime

    elif curAction == 'acquire':
        if cpuState[curCpu] != 'try':
            print('acquire before try at line %d' % (fileLine))
            print('|->cur:\t%s' % (curLine))
            print('|->sta: %s\ttry: %f\tacq: %f\tunlock: %f' % (cpuState[curCpu], cpuTry[curCpu], cpuAcquire[curCpu], cpuUnlock[curCpu]))
        cpuState[curCpu] = curAction
        cpuAcquire[curCpu] = curTime

        plt.barh(curCpu, cpuAcquire[curCpu]-cpuTry[curCpu], left=cpuTry[curCpu], height=0.8, facecolor='tan')

    elif curAction == 'unlock':
        if cpuState[curCpu] != 'acquire':
            print('unlock before acquire at line %d' % (fileLine))
            print('|->cur:\t%s' % (curLine))
            print('|->sta: %s\ttry: %f\tacq: %f\tunlock: %f' % (cpuState[curCpu], cpuTry[curCpu], cpuAcquire[curCpu], cpuUnlock[curCpu]))
        cpuState[curCpu] = curAction
        cpuUnlock[curCpu] = curTime

        plt.barh(curCpu, cpuUnlock[curCpu]-cpuAcquire[curCpu], left=cpuAcquire[curCpu], height=0.8, facecolor='blue')

curFile.close()
    
plt.show()
