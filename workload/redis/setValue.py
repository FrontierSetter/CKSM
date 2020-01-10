import redis
import time
import sys


portNum = int(sys.argv[1])
num = int(sys.argv[2])
conn = redis.Redis(host='192.168.198.164',port=portNum)

print (int(time.time()))

for i in range(num):
    if i%10000 == 0:
        print(i)
    conn.set('key'+str(i),'value'+str(i)) # 向远程redis中写入了一个键值对
    # time.sleep(0.00001)
    # val = conn.get('key'+str(i)) # 获取键值对
    # print(val)

print('finish'+str(portNum))