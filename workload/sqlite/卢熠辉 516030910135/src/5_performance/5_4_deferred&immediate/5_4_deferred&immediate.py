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

    operateNum = []
    timeDeferred = []
    timeImmediate = []
    timeExclusive = []

    while globalIdx <= edNum:

        f = open('deferred.db', 'w')
        f.close()
        f = open('immediate.db', 'w')
        f.close()
        f = open('exclusive.db', 'w')
        f.close()

        connDeffer = sqlite3.connect('deferred.db', 5.0, 0, 'DEFERRED')
        connImmediate = sqlite3.connect('immediate.db', 5.0, 0, 'IMMEDIATE')
        connExclusive = sqlite3.connect('exclusive.db', 5.0, 0, 'EXCLUSIVE')

        curDeffer = connDeffer.cursor()
        curImmediate = connImmediate.cursor()
        curExclusive = connExclusive.cursor()

        curDeffer.execute('''CREATE TABLE STUDENT
            (ID  INT PRIMARY KEY     NOT NULL,
            NAME         CHAR(30)    NOT NULL,
            AGE          INT,
            GENDER       CHAR,
            MAJOR        CHAR(10));''')
        connDeffer.commit()

        curImmediate.execute('''CREATE TABLE STUDENT
            (ID  INT PRIMARY KEY     NOT NULL,
            NAME         CHAR(30)    NOT NULL,
            AGE          INT,
            GENDER       CHAR,
            MAJOR        CHAR(10)    );''')
        connImmediate.commit()

        curExclusive.execute('''CREATE TABLE STUDENT
            (ID  INT PRIMARY KEY     NOT NULL,
            NAME         CHAR(30)    NOT NULL,
            AGE          INT,
            GENDER       CHAR,
            MAJOR        CHAR(10)    );''')
        connExclusive.commit()

        print('make data')
        for i in range(step):
            fakeData.append([globalIdx]+fakeStudent)
            globalIdx += 1
        operateNum.append(len(fakeData))
        print(len(fakeData))

        stTime = time.perf_counter()
        for student in fakeData:
            curDeffer.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
                VALUES (?, ?, ?, ?, ? )", student)
            connDeffer.commit()
        edTime = time.perf_counter()
        timeDeferred.append(edTime-stTime)

        stTime = time.perf_counter()
        for student in fakeData:
            curImmediate.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
                VALUES (?, ?, ?, ?, ? )", student)
            connImmediate.commit()
        edTime = time.perf_counter()
        timeImmediate.append(edTime-stTime)

        stTime = time.perf_counter()
        for student in fakeData:
            curExclusive.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
                VALUES (?, ?, ?, ?, ? )", student)
            connExclusive.commit()
        edTime = time.perf_counter()
        timeExclusive.append(edTime-stTime)

        connDeffer.close()
        connImmediate.close()
        connExclusive.close()


    print('operateNum')
    print(operateNum)

    print('timeDeferred')
    print(timeDeferred)

    print('timeImmediate')
    print(timeImmediate)

    print('timeExclusive')
    print(timeExclusive)

    f1 = open('testData\\testData'+str(round), 'w')
    f1.write(str(len(operateNum))+'\n')

    for num in operateNum:
        f1.write(str(num)+'\n')
    for num in timeDeferred:
        f1.write(str(num)+'\n')
    for num in timeImmediate:
        f1.write(str(num)+'\n')
    for num in timeExclusive:
        f1.write(str(num)+'\n')
            
    f1.close()
