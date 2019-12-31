import numpy as np  
import matplotlib.mlab as mlab  
import matplotlib.pyplot as plt

fileName = input('File: ')
curFile = open(fileName, 'r')

Y = []

while True:
    curLine = curFile.readline().strip('\n')
    if curLine == '':
        break
    Y.append(10)

X = range(len(Y))

print(Y)
print(X)
 
# X=[0,1,2,3,4,5]
# Y=[222,42,455,664,454,334]  
fig = plt.figure()
plt.bar(X,Y,0.4,color="green")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("bar chart")
  
 
plt.show()  
