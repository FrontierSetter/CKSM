import sys
import matplotlib.pyplot as plt

# python .\dedi_pattern_mapcnt_ngi.py '..\log\8-26-3(nginx32_scan_pattern)\diff_out_total.log'

inputFile = open(sys.argv[1], 'r')

baseArr = inputFile.readline().strip('\n').split()
baseTime = int(baseArr[0])
endTime = int(baseArr[1]) if len(baseArr) > 1 else 99999
scaleTimeFactor = float(baseArr[2]) if len(baseArr) > 2 else 1.0
scaleMemFactor = float(baseArr[3]) if len(baseArr) > 3 else 1.0

timeArr = []
globalArr = []
localArr = []

golbalThreshold = 1024

while True:
    curLine = inputFile.readline()
    
    if curLine == '':
        break

    curTime = int(curLine)

    if curTime < baseTime:
        while True:
            curLine = inputFile.readline()
            if curLine == '\n':
                break
        continue

    curGlobal = 0
    curLocal = 0
    curStamp = int((curTime-baseTime)*scaleTimeFactor)

    if curStamp > endTime:
        break

    curLine = inputFile.readline()
    curLineArr = curLine.strip('\n').split()
    curGlobal += int(curLineArr[1])

    while True:
        curLine = inputFile.readline()
        if curLine == '\n':
            break

        curLineArr = curLine.strip('\n').split()

        curIdx = int(curLineArr[0])
        curCnt = int(curLineArr[1])

        if curIdx < 0:
            continue
        elif curIdx <= golbalThreshold:
            curLocal += curCnt
        else:
            curGlobal += curCnt

    if curStamp in timeArr:
        continue

    timeArr.append(curStamp)
    globalArr.append(curGlobal*4.0/1024.0/1024.0*scaleMemFactor)
    localArr.append(curLocal*4.0/1024.0/1024.0*scaleMemFactor)


width = 0.8

globalTotal = 0
localTotal = 0

for i in globalArr:
    globalTotal += i

for i in localArr:
    localTotal += i

print(globalTotal)
print(localTotal)

plt.figure(figsize=(9,6))

legendEntryArr = ['Local Pattern', 'Global Pattern']
legendArr = [
    plt.bar(timeArr, localArr, width, bottom=globalArr, color='#C00000', label='Local Pattern'),
    plt.bar(timeArr, globalArr, width, color='#1f497d', label='Global Pattern')
]
plt.legend( fontsize=22)
# plt.legend(legendArr, legendEntryArr, fontsize=22)

# xfmt = ScalarFormatter(useMathText=True)
# xfmt.set_powerlimits((0, 0))
# plt.gca().yaxis.set_major_formatter(xfmt)
plt.xlim(-3,timeArr[-1])
plt.ylabel('Memory Merged(GB)', fontsize=26)
plt.xlabel('Time(s)', fontsize=26)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.subplots_adjust(left=0.125, right=0.99, top=0.99, bottom=0.12)

plt.savefig('map_count_nginx_32.pdf')

plt.show()