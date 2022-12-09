from flask import Flask, render_template, request, session, redirect, jsonify
import os
import pymysql
import json
import bcrypt

from flask_paginate import Pagination, get_page_args

# from werkzeug.utils import secure_filename
# UPLOAD_FOLDER = 'static/img'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)
app.config["SECRET_KEY"] = "abcd"


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# main
@app.route('/')
def home():
    per_page = 6
    page, _, offset = get_page_args(per_page = per_page)  # page 기본값 1 offset 0 _ 뜻은 per paper / 포스트 10개씩 페이지네이션
    print(page, _, offset)

    db = pymysql.connect(host='localhost', user='root', db='i_log', password='abc1234', charset='utf8')

    # db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_one',
    #                      password = 'M@ansghkwo12', charset = 'utf8')

    curs = db.cursor()

    curs.execute("SELECT COUNT(*) FROM post;")

    all_count = curs.fetchall()[0][0]
    curs.execute("SELECT * FROM post ORDER BY `created_at` ASC LIMIT %s OFFSET %s;", (per_page, offset))
    data_list = curs.fetchall()

    db.commit()
    db.close()

    pagination = Pagination(page = page, per_page = per_page, total = all_count, record_name = 'post',
                            css_framework = 'foundation', bs_version = 5)

    #
    # if "id" not in session:
    #     id = None;
    #     name = None;
    #     return render_template('main.html', data_lists=data_list, pagination=pagination, id=id, name=name)
    #
    # return render_template('main.html', data_lists=data_list, pagination=pagination, id=session["id"],
    #                        name=session["name"], css_framework='foundation', bs_version=5)
    #
    if "name" in session:
        return render_template('main.html', data_lists = data_list, pagination = pagination, name = session.get("name"),
                               login = True)
    else:
        return render_template('main.html', data_lists = data_list, pagination = pagination, login = False)


# ##메인페이지에 찎어주자구
# @app.route('/feed', methods=['GET'])
# def get_posts():
#     db = pymysql.connect(host='database-1.cbegjfm38p8o.ap-northeast-2.rds.amazonaws.com', user='admin', db='ione',
#                          password='ione1234', charset='utf8')
#     curs = db.cursor()
#
#     sql = "select * from post"
#     print(sql)
#
#     curs.execute(sql)
#
#     rows = curs.fetchall()
#     print(rows)
#
#     json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
#     db.commit()
#     db.close()
#     return json_str, 200
#


# login
@app.route('/users/login', methods = ['GET', 'POST'])
def login():
    db = pymysql.connect(host='localhost', user='root', db='i_log', password='abc1234', charset='utf8')

    # db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_one',
    #                      password = 'M@ansghkwo12', charset = 'utf8')

    curs = db.cursor()

    if request.method == 'POST':
        uid = request.form['userId']
        upw = request.form['password']

        session['uid'] = request.form['userId']

        # print('Login OKAY!')
        # print(session['uid'])
        # print(session['password'])
        # print(session)

        # print(session['uid'])

        curs.execute("SELECT * FROM user")

        user_list = curs.fetchall()

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
        db = pymysql.connect(host='localhost', user='root', db='i_log', password='abc1234', charset='utf8')

        # db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_one',
        #                      password = 'M@ansghkwo12', charset = 'utf8')
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
        db = pymysql.connect(host='localhost', user='root', db='i_log', password='abc1234', charset='utf8')

        # db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_one',
        #                      password = 'M@ansghkwo12', charset = 'utf8')
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
    db = pymysql.connect(host='localhost', user='root', db='i_log', password='abc1234', charset='utf8')

    # db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_one',
    #                      password = 'M@ansghkwo12', charset = 'utf8')
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


# write 글쓰기 페이지
@app.route('/write')
def write():
    if "name" not in session:
        # flash("로그인을 하세요!!")
        return render_template("login.html")


    else:
        "name" in session
    return render_template('write.html', id = session.get("uid"), name = session.get("name"), login = True)

    # return render_template('write.html', id = session.get("user"), name=session.get("name"), login=True)
    # if "name" in session:
    #     return render_template('write.html', name = session.get("name"), login = True)
    # else:
    #     return render_template('write.html', login = False)


# write 에서 포스팅하기
@app.route('/write', methods = ['POST'])
def insertpost():


    db = pymysql.connect(host='localhost', user='root', db='i_log', password='abc1234', charset='utf8')

    # db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_one',
    #                      password = 'M@ansghkwo12', charset = 'utf8')
    curs = db.cursor()
    print(session.get("uid"))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        content_image = request.form['content_image']
        user_id = session.get("uid")
        # user_id = session.get("name")

        sql = """insert into post (title, content, content_image, user_id)
         values (%s,%s,%s,%s)
        """
        curs.execute(sql, (title, content, content_image, user_id))

        db.commit()
        db.close()

        return redirect("/")


# 게시글 페이지 보여주기

@app.route('/post/<id>', methods = ['GET'])
def post(id):


    db = pymysql.connect(host='localhost', user='root', db='i_log', password='abc1234', charset='utf8')

    # db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_one',
    #                      password = 'M@ansghkwo12', charset = 'utf8')
    curs = db.cursor()
    # 나는 이 db를 선택하겠다 커서로 명령어를 내리는 것이다.

    sql = f"SELECT * FROM post WHERE id = '{id}'"
    # sql = f"SELECT * FROM post WHERE id > 0
    # sql 문 실행완료
    curs.execute(sql)
    # fectchall() 이거슬 전부다 rows에 담아줘  전부다가 fetchall() select문에서만 fetchall을 사용할 수 있다. insert update는 값을 변경하는 것이에 그 값을 출력할 필요가 없다.
    #fectchone()

    rows = curs.fetchall()
    list = []
    for row in rows:
        list.append(row)
        print(list)
    db.commit()
    db.close()
    return render_template('detail.html', list = list)


# edit 페이지 보여주기

@app.route('/edit/<id>', methods = ['GET'])
def correction(id):
    if "name" not in session:
        # flash("로그인을 하세요!!")
        return render_template("login.html")

    # else:
    #     "user_id" in session
    # return render_template('edit.html', id=session.get("uid"), name=session.get("name"), login=True)
    # #
    # if "user_id" not in session:
    #     # flash("로그인을 하세요!!")
    #     return render_template("login.html")

    db = pymysql.connect(host='localhost', user='root', db='i_log', password='abc1234', charset='utf8')

    # db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_one',
    #                      password = 'M@ansghkwo12', charset = 'utf8')
    curs = db.cursor()

    sql = f"SELECT * FROM post WHERE id = '{id}'"

    curs.execute(sql)

    rows = curs.fetchall()
    list = []
    for row in rows:
        list.append(row)

    db.commit()
    db.close()
    return render_template('edit.html', list = list)


# 수정된 게시글을 post방식으로 DB에 보내주기

@app.route('/edit/<id>', methods = ['POST'])
def edit(id):


    db = pymysql.connect(host='localhost', user='root', db='i_log', password='abc1234', charset='utf8')

    # db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_one',
    #                      password = 'M@ansghkwo12', charset = 'utf8')
    curs = db.cursor()

    title = request.form["title"]
    content = request.form["content"]

    sql = f"UPDATE post SET title = %s, content = %s WHERE id = '{id}';"

    curs.execute(sql, (title, content))

    db.commit()
    db.close()

    return redirect(f'/post/{id}')


# 게시글 삭제하기

@app.route("/delete/<id>", methods = ["GET", "POST", "DELETE"])
def delete_post(id):

    if "user_id" not in session:
        # flash("로그인을 하세요!!")
        return render_template("login.html")


    db = pymysql.connect(host='localhost', user='root', db='i_log', password='abc1234', charset='utf8')
    # db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_one',
    #                      password = 'abc1234', charset = 'utf8')
    curs = db.cursor()

    sql = f"DELETE FROM post WHERE id = '{id}'"
    curs.execute(sql)

    db.commit()
    db.close()
    # flash("삭제 완료")

    return redirect('/')


@app.route('/logout')
def logout():
    session.pop("name")
    return redirect("/")


# 서버실행
if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 5000, debug = True)
