from matplotlib import pyplot as plt  
from math import log
import cmath

# partial_hash_cc/partialHash.log

# filePath = input('file: ')
filePath = 'partial_hash_cc/partialHash.log'
curFile = open(filePath, 'r')

row = 32

X = []  

for i in range(row):
    X.append([])

curPos = 0


while True:
    curLine = curFile.readline().strip('\n')
    if curLine == '':
        break
    tem = int(curLine)
    pro = log(tem+1,2)
    # pro = tem
    # pro = tem ** 0.5
    X[curPos%row].append(pro)
    curPos += 1
    if curPos == 4096:
        break

print(X)

yIdx = [0, 8, 16, 24]
yNum = ['0x00', '0x08', '0x10', '0x18']

xIdx = []
xNum = []

for i in range(0, 128, 16):
    xIdx.append(i)

for i in xIdx:
    if i == 0:
        xNum.append('0x00')
    # xNum.append('%#03x'%(i*row))
    else:
        # xNum.append(hex(i*row))
        xNum.append(hex(i))

plt.figure(figsize=(9,6))
plt.subplots_adjust(left=0.12, right=0.99, top=0.96, bottom=0.12, hspace=0.36)

plt.gca().xaxis.set_ticks_position('top')

plt.imshow(X, cmap=plt.cm.hot)  
# plt.xticks
# plt.xticks([x for x in range(int(4096/row)) if x % 32 == 0], fontsize=12)
# plt.yticks([y for y in range(int(row)) if y % 8 == 0], fontsize=12)
plt.xticks(xIdx, xNum, fontsize=16)
plt.yticks(yIdx, yNum, fontsize=16)

plt.xlabel('Byte Address 7MSB', fontsize=18)
plt.ylabel('Byte Address 5LSB', fontsize=18)

# plt.colorbar()
plt.savefig('HeatMap.pdf')
plt.show() 