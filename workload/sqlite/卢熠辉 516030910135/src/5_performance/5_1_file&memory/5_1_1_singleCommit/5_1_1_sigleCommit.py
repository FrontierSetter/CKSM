import time
import sqlite3

totalFile = 10

stNum = int(input('start from: '))
edNum = int(input('end at: '))
step = int(input('step length: '))

for round in range(totalFile):
    fakeStudent = ['QYF', 21, 'M', 'EE']
    fakeData = []
    globalIdx = 1

    while globalIdx <= stNum:
        fakeData.append([globalIdx]+fakeStudent)
        globalIdx += 1

    timeMemory = []
    timeFile = []
    operateNum = []

    while globalIdx <= edNum:

        f = open('test.db', 'w')
        f.close()

        connMem = sqlite3.connect(':memory:')
        connFile = sqlite3.connect('test.db')

        curMem = connMem.cursor()
        curFile = connFile.cursor()

        curMem.execute('''CREATE TABLE STUDENT
        (ID  INT PRIMARY KEY     NOT NULL,
        NAME         CHAR(30)    NOT NULL,
        AGE          INT,
        GENDER       CHAR,
        MAJOR        CHAR(10)    );''')
        connMem.commit()

        curFile.execute('''CREATE TABLE STUDENT
            (ID  INT PRIMARY KEY     NOT NULL,
            NAME         CHAR(30)    NOT NULL,
            AGE          INT,
            GENDER       CHAR,
            MAJOR        CHAR(10)    );''')
        connFile.commit()

        print('make data')
        for i in range(step):
            fakeData.append([globalIdx]+fakeStudent)
            globalIdx += 1
        operateNum.append(len(fakeData))
        print(len(fakeData))

        stTime = time.perf_counter()
        curMem.executemany("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
            VALUES (?, ?, ?, ?, ? )", fakeData)
        connMem.commit()
        edTime = time.perf_counter()
        timeMemory.append(edTime-stTime)

        stTime = time.perf_counter()
        curFile.executemany("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
            VALUES (?, ?, ?, ?, ? )", fakeData)
        connFile.commit()
        edTime = time.perf_counter()
        timeFile.append(edTime-stTime)

        connMem.close()
        connFile.close()


    print('operateNum')
    print(operateNum)

    print('timeMemory')
    print(timeMemory)

    print('timeFile')
    print(timeFile)

    f1 = open('testData\\testData'+str(round), 'w')
    f1.write(str(len(operateNum))+'\n')

    for num in operateNum:
        f1.write(str(num)+'\n')
    for num in timeMemory:
        f1.write(str(num)+'\n')
    for num in timeFile:
        f1.write(str(num)+'\n')
            
    f1.close()
