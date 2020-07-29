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

cursorList = []

conn1 = sqlite3.connect('test.db')
print('conn1 Open')
outputFile.write('conn1 Open\n')

cursor1 = conn1.cursor()
print('cursor1 created')
outputFile.write('cursor1 created\n')


cursorList.append(cursor1)
for i in range(len(cursorList)):
    print('cursor%d read as:' % (i+1))
    outputFile.write('cursor%d read as:\n' % (i+1))
    for row in cursorList[i].execute('SELECT * FROM STUDENT'):
        print(row)
        outputFile.write('%d\t%s\t%d\t%s\t%s\n' % tuple(row))
    print()
    outputFile.write('\n')

cursor1.executemany("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
        VALUES (?, ?, ?, ?, ? )", studentList2)
print('cursor1 Insert 5,6')
outputFile.write('cursor1 Insert 5,6\n')
cursorList.append(conn1.cursor())
print('cursor%d created' % len(cursorList))
outputFile.write('cursor%d created\n' % len(cursorList))
for i in range(len(cursorList)):
    print('cursor%d read as:' % (i+1))
    outputFile.write('cursor%d read as:\n' % (i+1))
    for row in cursorList[i].execute('SELECT * FROM STUDENT'):
        print(row)
        outputFile.write('%d\t%s\t%d\t%s\t%s\n' % tuple(row))
    print()
    outputFile.write('\n')

cursor1.execute("DELETE from STUDENT where MAJOR='OW'")
print('cursor1 Delete 3,4')
outputFile.write('cursor1 Delete 3,4\n')
cursorList.append(conn1.cursor())
print('cursor%d created' % len(cursorList))
outputFile.write('cursor%d created\n' % len(cursorList))
for i in range(len(cursorList)):
    print('cursor%d read as:' % (i+1))
    outputFile.write('cursor%d read as:\n' % (i+1))
    for row in cursorList[i].execute('SELECT * FROM STUDENT'):
        print(row)
        outputFile.write('%d\t%s\t%d\t%s\t%s\n' % tuple(row))
    print()
    outputFile.write('\n')

conn1.commit()
print('conn1 Commit')
outputFile.write('conn1 Commit\n')
cursorList.append(conn1.cursor())
print('cursor%d created' % len(cursorList))
outputFile.write('cursor%d created\n' % len(cursorList))
for i in range(len(cursorList)):
    print('cursor%d read as:' % (i+1))
    outputFile.write('cursor%d read as:\n' % (i+1))
    for row in cursorList[i].execute('SELECT * FROM STUDENT'):
        print(row)
        outputFile.write('%d\t%s\t%d\t%s\t%s\n' % tuple(row))
    print()
    outputFile.write('\n')

for cursor in cursorList:
    print(id(cursor))

conn1.close()