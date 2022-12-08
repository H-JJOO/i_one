import os

import bcrypt
import pymysql
from flask import Flask, render_template, request, session, redirect, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config["SECRET_KEY"] = "abcd"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    db = pymysql.connect(host = 'database-1.cbegjfm38p8o.ap-northeast-2.rds.amazonaws.com', user = 'admin', db = 'ione',
                         password = 'ione1234', charset = 'utf8')
    curs = db.cursor()

    if request.method == 'POST':
        uid = request.form['userId']
        upw = request.form['password']

        # print(uid, upw)

        curs.execute("SELECT * FROM user")

        user_list = curs.fetchall()

        # print(user_list)

        for user in user_list:
            if uid == user[1]:
                if bcrypt.checkpw(upw.encode('utf-8'), user[2].encode('utf-8')):
                    session["name"] = user[3]
                    session["userid"] = user[1]
                    session["id"] = user[0]
                    return redirect("/")
                else:
                    return '<script>alert("비밀번호가 일치하지 않습니다."); document.location.href="login"; </script>'
        return '<script>alert("존재하지 않는 아이디입니다.."); document.location.href="login"; </script>'

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
    if "name" in session:
        return render_template('mypage.html', name = session.get("name"), login = True)
    return render_template("mypage.html")


# 프로필 수정 페이지
@app.route('/mypage/edit')
def mypage_edit():
    return render_template("mypage_edit.html")


# 페이지 DB GET 정보
@app.route('/users/<id>', methods = ['GET'])
def get_users(id):
    if "name" in session:
        db = pymysql.connect(host = 'database-1.cbegjfm38p8o.ap-northeast-2.rds.amazonaws.com', user = 'admin',
                             db = 'ione', password = 'ione1234', charset = 'utf8')
        curs = db.cursor()

        sql = '''SELECT user_id, name, gender, email, location, profile_image, intro FROM `user`'''

        curs.execute(sql)

        rows = curs.fetchall()

        # [session['id'] - 1] : 세션에 id 값이 담기는데 index 값보다 1이 많아서 -1 해줬습니다~

        result = {
            "user_id": rows[session['id'] - 1][0],
            "name": rows[session['id'] - 1][1],
            "gender": rows[session['id'] - 1][2],
            "email": rows[session['id'] - 1][3],
            "location": rows[session['id'] - 1][4],
            "profile_image": rows[session['id'] - 1][5],
            "intro": rows[session['id'] - 1][6]
        }

        db.commit()
        db.close()

        return jsonify({'users': result}), 200


# user DB 수정
@app.route('/users/<id>', methods = ["PUT"])
def put_users(id):
    if "name" in session:
        db = pymysql.connect(host = 'database-1.cbegjfm38p8o.ap-northeast-2.rds.amazonaws.com', user = 'admin',
                             db = 'ione', password = 'ione1234', charset = 'utf8')
        curs = db.cursor()

        name = request.form["name"]
        email = request.form["email"]
        intro = request.form["intro"]
        # file = request.files['file']
        #
        # if file.filename == '':
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #
        # profile_image = file.filename

        # sql = '''UPDATE `user` SET name=%s, email=%s, intro=%s, profile_image=%s WHERE id =%s'''

        sql = '''UPDATE `user` SET name=%s, email=%s, intro=%s WHERE id =%s'''

        # curs.execute(sql, (name, email, intro, profile_image, session["id"]))

        curs.execute(sql, (name, email, intro, session["id"]))

        session["name"] = name

        db.commit()
        db.close()

        return jsonify({'msg': '수정이 완료되었습니다'}), 200


# sign up, INSERT
@app.route('/users/signup', methods = ['POST'])
def insertuser():
    db = pymysql.connect(host = 'database-1.cbegjfm38p8o.ap-northeast-2.rds.amazonaws.com', user = 'admin', db = 'ione',
                         password = 'ione1234', charset = 'utf8')
    curs = db.cursor()

    if request.method == 'POST':
        uid = request.form['userId']
        upw = request.form['password']

        enc_upw = (bcrypt.hashpw(upw.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')

        nm = request.form['name']
        gender = request.form['gender']
        email = request.form["email"]
        loc = request.form['location']
        intro = request.form['intro']

        sql = """insert into user (user_id, password, name, gender, email, location, intro)
         values (%s,%s,%s,%s,%s,%s,%s)
        """

        # 중복 아이디 이메일 처리

        curs.execute("SELECT * FROM user")

        user_list = curs.fetchall()

        for user in user_list:
            if uid == user[1]:
                return '<script>alert("중복된 아이디 입니다."); document.location.href="signup";</script>'
            if email == user[5]:
                return '<script>alert("중복된 이메일 입니다."); document.location.href="signup";</script>'

        # 중복 아이디 이메일 처리

        curs.execute(sql, (uid, enc_upw, nm, gender, email, loc, intro))

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
