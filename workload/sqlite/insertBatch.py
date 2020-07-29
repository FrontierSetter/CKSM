import sqlite3
import sys

conn = sqlite3.connect(':memory:')


c = conn.cursor()

c.execute('''CREATE TABLE STUDENT
       (ID  INT PRIMARY KEY     NOT NULL,
       NAME         CHAR(30)    NOT NULL,
       AGE          INT,
       GENDER      CHAR,
       MAJOR        CHAR(10)    );''')

for i in range(int(sys.argv[1])):
    c.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
        VALUES (?, ?, ?, ?, ? )", (i, 'Laurie', 21, 'F', 'CS'))

conn.commit()