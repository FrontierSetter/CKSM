import sqlite3
import threading
import traceback
import time

f = open('db', 'w')
f.close()

outputFile = open('testData', 'w')

isolationLevel = ['DEFERRED', 'IMMEDIATE', 'EXCLUSIVE']
formerState = ['DoNothing', 'Read', 'Uncommitted', 'Committed']
latterBehaviour = ['Read', 'Write-Un', 'Write-Co']

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
SQL_createTable = '''CREATE TABLE STUDENT
                        (ID  INT PRIMARY KEY     NOT NULL,
                        NAME         CHAR(30)    NOT NULL,
                        AGE          INT,
                        GENDER       CHAR,
                        MAJOR        CHAR(10));'''
SQL_insertTuple = "INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
                        VALUES (?, ?, ?, ?, ? )"
SQL_selectTuple = "SELECT * FROM STUDENT"

for former in range(3):
    for latter in range(3):
        for state in range(4):
            for behavior in range(3):
                outputFile.write('\n%s\t%s\t%s\t%s\n' % (isolationLevel[former], formerState[state], isolationLevel[latter], latterBehaviour[behavior]))
                print('\n%s\t%s\t%s\t%s\n' % (isolationLevel[former], formerState[state], isolationLevel[latter], latterBehaviour[behavior]))
                # print(isolationLevel[former], formerState[state], isolationLevel[latter], latterBehaviour[behavior])
                f = open('db', 'w')
                f.close()

                conn0 = sqlite3.connect('db')
                conn0.execute(SQL_createTable)
                conn0.executemany(SQL_insertTuple, studentList0)
                conn0.commit()
                conn0.close()
                time.sleep(1)

                conn1 = sqlite3.connect('db', 5.0, 0, isolationLevel[former])
                if state == 0:
                    pass
                elif state == 1:
                    conn1.execute("SELECT * FROM STUDENT")
                elif state == 2:
                    conn1.executemany(SQL_insertTuple, studentList1)
                elif state == 3:
                    conn1.executemany(SQL_insertTuple, studentList1)
                    conn1.commit()

                try:
                    conn2 = sqlite3.connect('db', 5.0, 0, isolationLevel[latter])
                    if behavior == 0:
                        conn2.execute("SELECT * FROM STUDENT")
                    elif behavior == 1:
                        conn2.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) VALUES (5, 'QYF', 21, 'M', 'DNF')")
                    elif behavior == 2:
                        conn2.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) VALUES (5, 'QYF', 21, 'M', 'DNF')")
                        conn2.commit()
                    outputFile.write('%s\n' % 'Success')
                    print('%s\n' % 'Success')
                    # print('Success')
                except Exception as e:
                    outputFile.write('%s\n' % traceback.format_exc())
                    print('%s\n' % traceback.format_exc())
                    # traceback.print_exc()

                conn1.close()
                conn2.close()
    

outputFile.close()

                

                


