import time
import sqlite3
import random
import copy

totalFile = 10

stNum = int(input('start from: '))
edNum = int(input('end at: '))
step = int(input('step length: '))

for round in range(totalFile):
    fakeStudent = ['QYF', 21, 'M', 'EE']
    fakeData = []
    idxArr = []

    globalIdx = 1

    while globalIdx <= stNum:
        fakeData.append([globalIdx, globalIdx]+fakeStudent)
        idxArr.append([globalIdx])
        globalIdx += 1

    timeInsert = []
    timeDelete = []
    timeDeleteMultiKey = []
    timeDeleteMultiKeyReverse = []
    # timeDeleteMultiKeyRandom = []
    # timeDeleteMultiNotKey = []
    operateNum = []

    while globalIdx <= edNum:

        f = open('test.db', 'w')
        f.close()

        connFile = sqlite3.connect('test.db')

        curFile = connFile.cursor()

        curFile.execute('''CREATE TABLE STUDENT
            (ID  INT PRIMARY KEY     NOT NULL,
            FAKEID       INT,
            NAME         CHAR(30)    NOT NULL,
            AGE          INT,
            GENDER       CHAR,
            MAJOR        CHAR(10)    );''')
        connFile.commit()

        print('make data')
        for i in range(step):
            fakeData.append([globalIdx, globalIdx]+fakeStudent)
            idxArr.append([globalIdx])
            globalIdx += 1
        operateNum.append(len(fakeData))
        print(len(fakeData))


        stTime = time.perf_counter()
        curFile.executemany("INSERT INTO STUDENT (ID,FAKEID,NAME,AGE,GENDER,MAJOR) \
            VALUES (?, ?, ?, ?, ?, ?)", fakeData)
        connFile.commit()
        edTime = time.perf_counter()
        timeInsert.append(edTime-stTime)

        stTime = time.perf_counter()
        curFile.execute("DELETE from STUDENT where NAME='QYF'")
        connFile.commit()
        edTime = time.perf_counter()
        timeDelete.append(edTime-stTime)

        curFile.executemany("INSERT INTO STUDENT (ID,FAKEID,NAME,AGE,GENDER,MAJOR) \
            VALUES (?, ?, ?, ?, ?, ?)", fakeData)
        connFile.commit()

        stTime = time.perf_counter()
        curFile.executemany("DELETE from STUDENT where ID=?", idxArr)
        connFile.commit()
        edTime = time.perf_counter()
        timeDeleteMultiKey.append(edTime-stTime)

        # curFile.executemany("INSERT INTO STUDENT (ID,FAKEID,NAME,AGE,GENDER,MAJOR) \
        #     VALUES (?, ?, ?, ?, ?, ?)", fakeData)
        # connFile.commit()

        # stTime = time.perf_counter()
        # curFile.executemany("DELETE from STUDENT where FAKEID=?", idxArr)
        # connFile.commit()
        # edTime = time.perf_counter()
        # timeDeleteMultiNotKey.append(edTime-stTime)

        curFile.executemany("INSERT INTO STUDENT (ID,FAKEID,NAME,AGE,GENDER,MAJOR) \
            VALUES (?, ?, ?, ?, ?, ?)", fakeData)
        connFile.commit()

        reverseIdxArr = copy.deepcopy(idxArr)
        reverseIdxArr.reverse()

        stTime = time.perf_counter()
        curFile.executemany("DELETE from STUDENT where ID=?", reverseIdxArr)
        connFile.commit()
        edTime = time.perf_counter()
        timeDeleteMultiKeyReverse.append(edTime-stTime)

        # curFile.executemany("INSERT INTO STUDENT (ID,FAKEID,NAME,AGE,GENDER,MAJOR) \
        #     VALUES (?, ?, ?, ?, ?, ?)", fakeData)
        # connFile.commit()

        # randomIdxArr = copy.deepcopy(idxArr)
        # random.shuffle(randomIdxArr)

        # stTime = time.perf_counter()
        # curFile.executemany("DELETE from STUDENT where ID=?", randomIdxArr)
        # connFile.commit()
        # edTime = time.perf_counter()
        # timeDeleteMultiKeyRandom.append(edTime-stTime)
        

        connFile.close()


    print('operateNum')
    print(operateNum)

    print('timeInsert')
    print(timeInsert)

    print('timeDelete')
    print(timeDelete)

    print('timeDeleteMultiKey')
    print(timeDeleteMultiKey)

    # print('timeDeleteMultiNotKey')
    # print(timeDeleteMultiNotKey)

    print('timeDeleteMultiKeyReverse')
    print(timeDeleteMultiKeyReverse)

    # print('timeDeleteMultiKeyRandom')
    # print(timeDeleteMultiKeyRandom)
    

    f1 = open('testData\\testData'+str(round), 'w')
    f1.write(str(len(operateNum))+'\n')

    for num in operateNum:
        f1.write(str(num)+'\n')
    for num in timeInsert:
        f1.write(str(num)+'\n')
    for num in timeDelete:
        f1.write(str(num)+'\n')
    for num in timeDeleteMultiKey:
        f1.write(str(num)+'\n')
    # for num in timeDeleteMultiNotKey:
    #     f1.write(str(num)+'\n') 
    for num in timeDeleteMultiKeyReverse:
        f1.write(str(num)+'\n')  
    # for num in timeDeleteMultiKeyRandom:
    #     f1.write(str(num)+'\n')  
            
    f1.close()