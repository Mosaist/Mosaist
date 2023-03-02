import pymysql

def connectsql() :
     db = pymysql.connect(host="localhost", user="root", passwd="test", db="notice_board", charset="utf8")
     return db

db=connectsql()
cur=db.cursor()
sql="INSERT INTO board (num,title,writer,posted, views,context) VALUES (NULL,%s,%s,DEFAULT,%s,%s)"
value=("입력테스트","김준호","10","제목 테스트 ")
cur.execute(sql,value)
db.commit()