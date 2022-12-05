from flask import Flask, render_template, request
import pymysql
import json

app = Flask(__name__)


# main
@app.route('/')
def root():
    return render_template('main.html')


# login
@app.route('/login')
def login():
    return render_template('login.html')


# sign up
@app.route('/signup')
def signup():
    return render_template('signup.html')

#마이페이지
@app.route('/mypage')
def mypage():
    return render_template('mypage.html')

#프로필 수정 페이지
@app.route('/setting')
def mypageSetting():
    return render_template('mypage_setting.html')

# sign up, INSERT
@app.route('/signup', methods = ['POST', 'GET'])
def insert_user():
    db = pymysql.connect(host = 'localhost', user = 'root', db = 'mysql', password = 'M@ansghkwo12', charset = 'utf8')
    curs = db.cursor()

    if request.method == 'POST':
        uid = request.form['name']
        upw = request.form['password']
        nm = request.form['name']
        gender = request.form['gender']
        email = request.form['email']
        loc = request.form['location']

        sql = """insert into t_user (uid, upw, nm, gender, email, location)
         values (%s,%s,%s,%s,%s,%s)
        """
        curs.execute(sql, (uid, upw, nm, gender))

        return 'insert success', 200

    user = request.json


# 서버실행
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)

