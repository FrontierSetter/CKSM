import sqlite3

outputFile = open('testData', 'w')

studentList0 = [
    [1, 'BYX', 17, 'F', 'DOTA'],
    [2, 'BYX', 20, 'M', 'DOTA'],
]
studentList1 = [
    [3, 'LZQ', 17, 'F', 'OW'],
    [4, 'LZQ', 20, 'M', 'OW'],
]
studentList2 = [
    [5, 'QYF', 17, 'F', 'DNF'],
    [6, 'QYF', 20, 'M', 'DNF'],
]

f = open('test.db', 'w')
f.close()

conn0 = sqlite3.connect('test.db')
conn0.execute('''CREATE TABLE STUDENT
        (ID  INT PRIMARY KEY     NOT NULL,
        NAME         CHAR(30)    NOT NULL,
        AGE          INT,
        GENDER       CHAR,
        MAJOR        CHAR(10));''')
conn0.executemany("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
        VALUES (?, ?, ?, ?, ? )", studentList0)
conn0.executemany("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
        VALUES (?, ?, ?, ?, ? )", studentList1)
conn0.commit()
conn0.close()

conn1 = sqlite3.connect('test.db')
print('conn1 Open')
outputFile.write('conn1 Open\n')

conn2 = sqlite3.connect('test.db')
print('conn2 Open')
outputFile.write('conn2 Open\n')

connList = [conn1, conn2]

conn2.executemany("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
        VALUES (?, ?, ?, ?, ? )", studentList2)
print('conn2 Insert 5,6')
outputFile.write('conn2 Insert 5,6\n')
for i in range(len(connList)):
    print('conn%d read as:' % (i+1))
    outputFile.write('conn%d read as:\n' % (i+1))
    for row in connList[i].execute('SELECT * FROM STUDENT'):
        print(row)
        outputFile.write('%d\t%s\t%d\t%s\t%s\n' % tuple(row))
    print()
    outputFile.write('\n')

conn2.execute("DELETE from STUDENT where MAJOR='OW'")
print('conn2 Delete 3,4')
outputFile.write('conn2 Delete 3,4\n')
for i in range(len(connList)):
    print('conn%d read as:' % (i+1))
    outputFile.write('conn%d read as:\n' % (i+1))
    for row in connList[i].execute('SELECT * FROM STUDENT'):
        print(row)
        outputFile.write('%d\t%s\t%d\t%s\t%s\n' % tuple(row))
    print()
    outputFile.write('\n')

conn2.commit()
print('conn2 Commit')
outputFile.write('conn2 Commit\n')
for i in range(len(connList)):
    print('conn%d read as:' % (i+1))
    outputFile.write('conn%d read as:\n' % (i+1))
    for row in connList[i].execute('SELECT * FROM STUDENT'):
        print(row)
        outputFile.write('%d\t%s\t%d\t%s\t%s\n' % tuple(row))
    print()
    outputFile.write('\n')