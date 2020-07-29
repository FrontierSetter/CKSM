import sqlite3

conn = sqlite3.connect(':memory:')

c = conn.cursor()

# =========================
# Stage 1 初始化数据并提交 
# =========================
c.execute('''CREATE TABLE STUDENT
       (ID  INT PRIMARY KEY     NOT NULL,
       NAME         CHAR(30)    NOT NULL,
       AGE          INT,
       GENDER      CHAR,
       MAJOR        CHAR(10)    );''')

c.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
      VALUES (1, 'QYF', 22, 'M', 'EE' )")

c.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER) \
      VALUES (2, 'LZQ', 22, 'M' )")

c.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
      VALUES (3, 'Mark', 12, 'F', 'CS' )")

c.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
      VALUES (4, 'Demi', 20, 'F', 'SE' )")

studentList1 = [
    (5, 'Laurie', 21, 'F', 'CS'),
    (6, 'Jonathan', 25, 'M', 'EE'),
]
for student in studentList1 :
    c.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
        VALUES (?, ?, ?, ?, ? )", student)

studentList2 = [
    [7, 'Hornby', 17, 'F', 'CS'],
    [8, 'Zephaniah', 20, 'M', 'EE'],
]
c.executemany("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
    VALUES (?, ?, ?, ?, ? )", studentList2)

conn.commit()
print("\nstage1 committed")
for row in c.execute("SELECT id, name, GENDER, MAJOR FROM STUDENT"):
   print(row)

# =========================
# Stage 2 修改数据不提交 
# =========================
c.executemany("DELETE from STUDENT where MAJOR=?", (('SE',), ('CS',)))

print("\nstage2 uncommitted")
for row in c.execute("SELECT id, name, GENDER, MAJOR FROM STUDENT"):
   print(row)

# =========================
# 数据库回滚 回到Stage 1
# =========================
conn.rollback()
print("\nrollback to stage1")
for row in c.execute("SELECT id, name, GENDER, MAJOR FROM STUDENT"):
   print(row)

# =========================
# Stage 3 修改数据不提交 
# =========================
c.executemany("DELETE from STUDENT where MAJOR=?", (('SE',), ('CS',)))

print("\nstage3 uncommitted")
for row in c.execute("SELECT id, name, GENDER, MAJOR FROM STUDENT"):
   print(row)

# ======================================
# Stage 4 使用executescript修改数据不提交 
# ======================================
c.executescript('''
    INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
        VALUES (9, 'NEWQYF', 22, 'M', 'CS' );
    
    INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
        VALUES (10, 'NEWLZQ', 21, 'M', 'CS');

    DELETE from STUDENT where MAJOR='EE';

''')
print("\nstage4 uncommitted")
for row in c.execute("SELECT id, name, GENDER, MAJOR FROM STUDENT"):
   print(row)

# ======================================
# 数据库回滚 回到（其实没动）Stage 4的状态 
# ======================================
conn.rollback()
print("\nrollback")
for row in c.execute("SELECT id, name, GENDER, MAJOR FROM STUDENT"):
   print(row)

# =========================
# Stage 3 修改数据不提交 
# =========================
c.executemany("DELETE from STUDENT where MAJOR=?", (('SE',), ('CS',)))

print("\nstage3 uncommitted")
for row in c.execute("SELECT id, name, GENDER, MAJOR FROM STUDENT"):
   print(row)

conn.commit()
conn.close()