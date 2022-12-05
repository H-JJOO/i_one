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


# sign up, INSERT
@app.route('/signup', methods = ['POST', 'GET'])
def insert_user():
    db = pymysql.connect(host = 'localhost', user = 'root', db = 'mysql', password = 'M@ansghkwo12', charset = 'utf8')
    curs = db.cursor()

    if request.method == 'POST':
        val = request.form
        return render_template("signup.html", result = val)

    user = request.json





# 서버실행
if __name__ == '__main__':
    app.run('0.0.0.0', port = 5000, debug = True)
