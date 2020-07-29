import sqlite3

conn = sqlite3.connect(':memory:')
print("connect success")

# 以下操作不再使用cursor对象，而是直接在connection对象上执行
# c = conn.cursor()

conn.execute('''CREATE TABLE STUDENT
       (ID  INT PRIMARY KEY     NOT NULL,
       NAME         CHAR(30)    NOT NULL,
       AGE          INT,
       GENDER      CHAR,
       MAJOR        CHAR(10)    );''')

print("create test success")

conn.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
      VALUES (1, 'QYF', 22, 'M', 'EE' )")

conn.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER) \
      VALUES (2, 'LZQ', 22, 'M' )") 

conn.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
      VALUES (3, 'Mark', 12, 'F', 'CS' )")

conn.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
      VALUES (4, 'Demi', 20, 'F', 'SE' )")

studentList1 = [
    (5, 'Laurie', 21, 'F', 'CS'),
    (6, 'Jonathan', 25, 'M', 'EE'),
]
for student in studentList1 :
    conn.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
        VALUES (?, ?, ?, ?, ? )", student)

studentList2 = [
    [7, 'Hornby', 17, 'F', 'CS'],
    [8, 'Zephaniah', 20, 'M', 'EE'],
]
conn.executemany("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
    VALUES (?, ?, ?, ?, ? )", studentList2)

print("insert success")

cursor = conn.execute("SELECT id, name, GENDER, MAJOR FROM STUDENT")

for row in cursor:
   print(row)

print("select success")

conn.execute("DELETE from STUDENT where MAJOR=?", ('SE',))
for row in conn.execute("SELECT id, MAJOR FROM STUDENT"):
   print(row)
print('delete success')

conn.execute("UPDATE STUDENT set MAJOR = 'SE' where MAJOR is NULL")
for row in conn.execute("SELECT id, MAJOR FROM STUDENT"):
   print(row)
print('update success')

conn.commit()

conn.close()