# 导入sqlite3模块
import sqlite3

# ==========================================
#                   目录
# 建立连接
# 获取游标
# 执行语句
##  创建表
##  单个插入
###     插入固定值
###     插入变量
##  批量插入
##  查询
###     迭代器游标
###     fetchone()
###     fetchall()
###     fetchmany(size)
##  删除
##  修改
# 提交修改
# 关闭连接
# ==========================================

# ==========================================
# 第一步 建立与数据库的链接
# ==========================================
# 可以使用内存数据库如： 
conn = sqlite3.connect(':memory:')
# 也可以使用本地文件作为数据库容器：
#conn = sqlite3.connect('mydb.db')
print("connect success")

# ==========================================
# 第二步 从连接创建游标对象，用于后续执行SQL语句
# ==========================================
c = conn.cursor()

# ==========================================
# 第三步 使用游标对象的方法执行SQL语句
# ==========================================

## -----------------------------------------
## 创建表
## CREATE TABLE
## -----------------------------------------
c.execute('''CREATE TABLE STUDENT
       (ID  INT PRIMARY KEY     NOT NULL,
       NAME         CHAR(30)    NOT NULL,
       AGE          INT,
       GENDER      CHAR,
       MAJOR        CHAR(10)    );''')

print("create success")

## -----------------------------------------
## 向表中逐个插入数据
## INSERT
## -----------------------------------------

### 插入固定值数据
c.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
      VALUES (1, 'QYF', 22, 'M', 'EE' )")

c.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER) \
      VALUES (2, 'LZQ', 22, 'M' )") # NONE值测试

c.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
      VALUES (3, 'Mark', 12, 'F', 'CS' )")

c.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
      VALUES (4, 'Demi', 20, 'F', 'SE' )")

### 从python变量获取参数
studentList1 = [
    (5, 'Laurie', 21, 'F', 'CS'),
    (6, 'Jonathan', 25, 'M', 'EE'),
]
for student in studentList1 :
    c.execute("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
        VALUES (?, ?, ?, ?, ? )", student)

## -----------------------------------------
## 向表中批量插入数据
## -----------------------------------------
studentList2 = [
    [7, 'Hornby', 17, 'F', 'CS'],
    [8, 'Zephaniah', 20, 'M', 'EE'],
]
c.executemany("INSERT INTO STUDENT (ID,NAME,AGE,GENDER,MAJOR) \
    VALUES (?, ?, ?, ?, ? )", studentList2)

print("insert success")

## -----------------------------------------
## 从表中查询数据
## SELECE
## -----------------------------------------
cursor = c.execute("SELECT id, name, GENDER, MAJOR FROM STUDENT")


### 将获取到的游标作为迭代器使用
for row in cursor:
   print(row)

### 使用fetchone()方法逐行获得查询结果，每次获得一个元组
while True:
    row = c.fetchone()
    if row == None:
        break
    else:
        print(row)

### 使用fetchall()方法获得全部剩余查询结果，获得一个元组的元组
rows = c.fetchall()
for row in rows:
    print(row)

### 使用fetchmany(size=cursor.arraysize)方法获得(不大于）指定长度的剩余结果，获得一个元组的元组
fetchNum = 3    # 使用一个不能整除8的数，测试当剩余数少于参数时的效果
while True:
    rows = c.fetchmany(fetchNum)
    if rows == []:
        break 
    else:
        for row in rows:
            print(row)
print("select success")

## -----------------------------------------
## 从表中删除数据
## DELETE
## -----------------------------------------
c.execute("DELETE from STUDENT where MAJOR=?", ('SE',)) # 注意提供的必须是一个可枚举类型（列表或元组）
for row in c.execute("SELECT id, MAJOR FROM STUDENT"):
   print(row)
print('delete success')

## -----------------------------------------
## 更新表中的数据
## UPDATE
## -----------------------------------------
c.execute("UPDATE STUDENT set MAJOR = 'SE' where MAJOR is NULL")    # 注意虽然空值在SQLite中显示是None，但判定时仍是NULL
for row in c.execute("SELECT id, MAJOR FROM STUDENT"):
   print(row)
print('update success')

# ==========================================
# 提交事务
# ==========================================
conn.commit()

# ==========================================
# 关闭连接
# ==========================================
conn.close()

