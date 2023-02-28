import os
import ssl
import json
from flask import Flask, render_template, send_file,url_for,request,redirect
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

@app.route('/list')
@app.route('/list.html')
def notice() :
    db=connectsql()
    cur = db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * from board ORDER BY num DESC"
    cur.execute(sql)
    data_list=cur.fetchall()
    return render_template('html/list.html', data_list=data_list, config=config)
@app.route('/list.html')
@app.route('/write', methods=['POST','GET'])
@app.route('/write.html', methods =['POST','GET'])
def write() :
    if request.method =='POST' :
         usertitle=request.form['title']
         writer=request.form['writer']
         usercontent=request.form['content']
         db=connectsql()
         cur=db.cursor()
         sql="INSERT INTO board (num,title,writer,posted, views,context) VALUES (NULL,%s,%s,DEFAULT,DEFAULT,%s)"
         value=(usertitle,writer,usercontent)
         cur.execute(sql,value)
         db.commit()
         cur.close()
         db.close()
         return redirect(url_for('html/list',config=config))
    return render_template('html/write.html',config=config)
@app.route('/list/view/<int:num>')
@app.route('/list/view.html/<int:num>')
def content(num) :
    db=connectsql()
    cur=db.cursor(pymysql.cursors.DictCursor)
    sql="SELECT * from board WHERE num = %s"
    value=num
    cur.execute(sql,value)
    data_list=cur.fetchall()
    return render_template('html/view.html',data_list=data_list, config=config)

@app.route('/list/edit/<int:num>',methods=['GET','POST'])
@app.route('/list/edit.html/<int:num>',methods=['GET','POST'])
def edit(num) :
    if request.method =='POST' :
        edittitle = request.form['title']
        editcontent=request.form['content']
        db=connectsql()
        cur=db.cursor()
        sql="UPDATE board SET title = %s, context = %s WHERE num= %s"
        value=(edittitle,editcontent,num)
        cur.execute(sql,value)
        db.commit()
        return render_template('html/edit.html',config=config)
    else :
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

        app.run(host=config['server']['ip'], port=config['server']['front']['port'], ssl_context=ssl_context, debug=True)
