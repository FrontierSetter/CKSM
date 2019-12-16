import struct

curFile = open('dataFile', 'wb')
fileSize = int(input('pageNum: '))
modNum = int(input('modwith: '))

for i in range(fileSize*1024):
    curFile.write(struct.pack('I', i%modNum))
