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
    timeExeMany = []
    timeOneCommit = []
    # timeMultiCommit = []

    while globalIdx <= edNum:

        # f = open('execute_multicommit.db', 'w')
        # f.close()
        f = open('execute_onecommit.db', 'w')
        f.close()
        f = open('executemany.db', 'w')
        f.close()

        connExeMany = sqlite3.connect('executemany.db')
        connOneCommit = sqlite3.connect('execute_onecommit.db')
        # connMultiCommit = sqlite3.connect('execute_multicommit.db')

        curExeMany = connExeMany.cursor()
        curOneCommit = connOneCommit.cursor()
        # curMultiCommit = connMultiCommit.cursor()

        curExeMany.execute('''CREATE TABLE STUDENT
            (ID  INT PRIMARY KEY     NOT NULL,
            NAME         CHAR(30)    NOT NULL,
            AGE          INT,
            GENDER       CHAR,
            MAJOR        CHAR(10));''')
        connExeMany.commit()

        curOneCommit.execute('''CREATE TABLE STUDENT
            (ID  INT PRIMARY KEY     NOT NULL,
            NAME         CHAR(30)    NOT NULL,
            AGE          INT,
            GENDER       CHAR,
            MAJOR        CHAR(10)    );''')
        connOneCommit.commit()

        # curMultiCommit.execute('''CREATE TABLE STUDENT
        #     (ID  INT PRIMARY KEY     NOT NULL,
        #     NAME         CHAR(30)    NOT NULL,
        #     AGE          INT,
        #     GENDER       CHAR,
        #     MAJOR        CHAR(10)    );''')
        # connMultiCommit.commit()

        print('make data')
        for i in range(step):
            fakeData.append([globalIdx]+fakeStudent)
            globalIdx += 1
        operateNum.append(len(fakeData))
        print(len(fakeData))

        stTime = time.perf_counter()
        curExeMany.executemany("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
            VALUES (?, ?, ?, ?, ? )", fakeData)
        connExeMany.commit()
        edTime = time.perf_counter()
        timeExeMany.append(edTime-stTime)

        stTime = time.perf_counter()
        for student in fakeData:
            curOneCommit.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
            VALUES (?, ?, ?, ?, ? )", student)
        connOneCommit.commit()
        edTime = time.perf_counter()
        timeOneCommit.append(edTime-stTime)

        # print("MC start")
        # stTime = time.perf_counter()
        # for student in fakeData:
        #     curMultiCommit.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
        #     VALUES (?, ?, ?, ?, ? )", student)
        #     connMultiCommit.commit()
        # edTime = time.perf_counter()
        # timeMultiCommit.append(edTime-stTime)
        # print("MC end")

        connExeMany.close()
        connOneCommit.close()
        # connMultiCommit.close()


    print('operateNum')
    print(operateNum)

    print('timeExeMany')
    print(timeExeMany)

    # print('timeMultiCommit')
    # print(timeMultiCommit)

    print('timeOneCommit')
    print(timeOneCommit)

    f1 = open('testData\\testData'+str(round), 'w')
    f1.write(str(len(operateNum))+'\n')

    for num in operateNum:
        f1.write(str(num)+'\n')
    for num in timeExeMany:
        f1.write(str(num)+'\n')
    # for num in timeMultiCommit:
    #     f1.write(str(num)+'\n')
    for num in timeOneCommit:
        f1.write(str(num)+'\n')
            
    f1.close()
