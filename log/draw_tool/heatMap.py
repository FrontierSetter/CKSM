from matplotlib import pyplot as plt  
from math import log
import cmath

# partial_hash_cc/partialHash.log

filePath = input('file: ')
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


plt.imshow(X, cmap=plt.cm.hot)  
plt.xticks([x for x in range(int(4096/row)) if x % 16 == 0], fontsize=12)
plt.yticks([y for y in range(int(row)) if y % 8 == 0], fontsize=12)
# plt.colorbar()
plt.savefig('HeatMap.pdf')
plt.show() 