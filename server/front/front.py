import os
import ssl
import json
from flask import Flask, render_template, send_file,url_for,request,redirect, jsonify
import pymysql


config = json.load(open(f'{os.path.dirname(__file__)}/../../config.json'))
"""
전역 환경 변수 모음
"""

app = Flask(__name__)

"""
플라스크 프론트 서버 인스턴스
"""
def connectsql() :
     db = pymysql.connect(host="localhost", user="root", passwd="test", db="notice_board", charset="utf8")
     return db


@app.route('/list.html')
def notice() :
    db=connectsql()
    cur = db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * from board ORDER BY num DESC"
    cur.execute(sql)
    data_list=cur.fetchall()


    return render_template('html/list.html', data_list=data_list, config=config)


@app.route('/write', methods=['POST', 'GET'])
def write():
    if request.method == 'POST':
        title = request.json["title"]
        writer = request.json["writer"]
        content = request.json["content"]
        try:
            db = connectsql()
            cur = db.cursor()
            sql = "INSERT INTO board (num,title,writer,posted, views,context) VALUES (NULL,%s,%s,DEFAULT,DEFAULT,%s)"
            value=(title,writer,content)
            cur.execute(sql,value)
            db.commit()
            cur.close()
            db.close()
            return jsonify(True)
        except Exception as e:
            return jsonify(False)

@app.route('/list/view/<int:num>')
@app.route('/list/view.html/<int:num>')
def content(num) :
    database=connectsql()
    cursor=database.cursor()
    query="UPDATE board SET views = views + 1 WHERE num = %s"
    val=num
    cursor.execute(query,val)
    database.commit()
    cursor.close()
    database.close()


    db=connectsql()
    cur=db.cursor(pymysql.cursors.DictCursor)
    sql="SELECT * from board WHERE num = %s"
    value=num
    cur.execute(sql,value)
    data_list=cur.fetchall()
    return render_template('html/view.html',data_list=data_list, config=config)



@app.route('/list/edit.html/<int:num>',methods=['GET','POST'])
def edit(num) :
    if request.method =='POST' :
        title = request.json["title"]
        writer = request.json["writer"]
        content = request.json["content"]
        db=connectsql()
        cur=db.cursor()
        sql="UPDATE board SET title = %s, writer = %s, context = %s WHERE num= %s"
        value=(title,writer,content,num)
        cur.execute(sql,value)
        db.commit()
        return jsonify(True)
    elif request.method=='GET' :
        db=connectsql()
        cur=db.cursor(pymysql.cursors.DictCursor)
        sql ="SELECT * FROM board WHERE num = %s"
        value=num
        cur.execute(sql,value)
        data_list=cur.fetchall()
        return render_template('html/edit.html',data_list=data_list, config=config)

@app.route('/')
def root():
    """
    최상위 도메인에 대한 응답 처리

    Returns:
        전처리된 HTML.
    """
    print('root')

    return render_template('html/index.html', config=config)

@app.route('/favicon.ico')
def favicon():
    print('hi')

@app.route('/<path:path>')
def template(path):
    """
    최상위 도메인에 대한 응답 처리

    Params:
        path: 요청 url.

    Returns:
        전처리된 HTML.
    """
    print(path)

    return render_template(f'html/{path}', config=config)

@app.route('/resource/<path:path>')
def resource(path):
    """
    리소스 요청에 대한 응답 처리

    Params:
        path: 요청 url.

    Returns:
        요청한 리소스.
    """

    return send_file(f'templates/assets/{path}')


if __name__ == '__main__':
    if config['server']['useProxy']:
        app.run(host='127.0.0.1', port=config['server']['front']['port'])
    else:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=config['server']['sslCert'], keyfile=config['server']['sslKey'])

        app.run(host=config['server']['ip'], port=config['server']['front']['port'], ssl_context=ssl_context)
