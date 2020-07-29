orilist = [1.1234213, 41234.431221, 432.4321]
f1 = open('testData', 'w')
for cur in orilist:
    f1.write(str(cur)+'\n')
f1.close()

nxtlist = []
f2 = open('testData', 'r')
for i in range(3):
    nxtlist.append(float(f2.readline()))

print(nxtlist)