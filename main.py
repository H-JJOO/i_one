from flask import Flask, render_template, request, session, redirect
import pymysql
import js2py
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "abcd"


# main
@app.route('/')
def home():
    if "name" in session:
        return render_template('main.html', name = session.get("name"), login = True)
    else:
        return render_template('main.html', login = False)


# login
@app.route('/users/login', methods = ['GET', 'POST'])
def login():
    db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_one', password = 'M@ansghkwo12', charset = 'utf8')
    curs = db.cursor()

    if request.method == 'POST':
        uid = request.form['userId']
        upw = request.form['password']

        print(uid, upw)

        curs.execute("SELECT * FROM user")

        user_list = curs.fetchall()

        print(user_list)

        for user in user_list:
            print(user)
            if uid == user[1]:
                if upw == user[2]:
                    session["name"] = user[3]
                    return redirect("/")
                else:
                    return '<script>alert("비밀번호가 틀렸습니다."); document.location.href="login"; </script>'
        return '<script>alert("아이디가 틀렸습니다."); document.location.href="login"; </script>'


        db.commit()
        db.close()

    return render_template('login.html')


# sign up
@app.route('/users/signup')
def signup():
    return render_template('signup.html')


# 마이페이지
@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


# 프로필 수정 페이지
@app.route('/setting')
def mypageSetting():
    return render_template('mypage_setting.html')


# sign up, INSERT
@app.route('/users/signup', methods = ['POST'])
def inseruser():
    db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_one', password = 'M@ansghkwo12', charset = 'utf8')
    curs = db.cursor()

    if request.method == 'POST':
        uid = request.form['userId']
        upw = request.form['password']
        nm = request.form['name']
        gender = request.form['gender']
        email = request.form["email"]
        loc = request.form['location']

        sql = """insert into user (user_id, password, name, gender, email, location)
         values (%s,%s,%s,%s,%s,%s)
        """
        curs.execute(sql, (uid, upw, nm, gender, email, loc))

        session["name"] = nm

        db.commit()
        db.close()

        return redirect("/")


@app.route('/logout')
def logout():
    session.pop("name")
    return redirect("/")


# 서버실행
if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 5000, debug = True)
