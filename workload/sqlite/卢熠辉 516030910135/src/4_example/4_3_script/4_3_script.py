import sqlite3

conn = sqlite3.connect(':memory:')
print("connect success")

c = conn.cursor()

# 使用executescript方法运行多条SQL指令
c.executescript('''
    CREATE TABLE STUDENT(
        ID  INT PRIMARY KEY     NOT NULL,
        NAME         CHAR(30)    NOT NULL,
        AGE          INT,
        GENDER      CHAR,
        MAJOR        CHAR(10)
    );

    INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
        VALUES (1, 'QYF', 22, 'M', 'EE' );
    
    INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
        VALUES (2, 'LZQ', 21, 'M', 'CS');

    DELETE from STUDENT where MAJOR='CS';

''')


for row in c.execute("SELECT id, MAJOR FROM STUDENT"):
   print(row)

conn.commit()

conn.close()