from flask import Flask, render_template, request, session, redirect
import pymysql
import json
import bcrypt

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
    db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_log', password = 'abc1234', charset = 'utf8')
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
                if bcrypt.checkpw(upw.encode('utf-8'), user[2].encode('utf-8')):
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
    db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_log', password = 'abc1234', charset = 'utf8')
    curs = db.cursor()

    if request.method == 'POST':
        uid = request.form['userId']
        upw = request.form['password']

        enc_upw = (bcrypt.hashpw(upw.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')

        nm = request.form['name']
        gender = request.form['gender']
        email = request.form["email"]
        loc = request.form['location']

        sql = """insert into user (user_id, password, name, gender, email, location)
         values (%s,%s,%s,%s,%s,%s)
        """
        curs.execute(sql, (uid, enc_upw, nm, gender, email, loc))

        session["name"] = nm

        db.commit()
        db.close()

        return redirect("/")




#write 에서 포스팅하기
@app.route('/write', methods = ['POST'])
def insertpost():
    db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_log', password = 'abc1234', charset = 'utf8')
    curs = db.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        content_image = request.form['content_image']
        user_id = 1
        created_at = 1
        updated_at = 1
        deleted = 0


        sql = """insert into post (title, content, content_image, user_id, created_at, updated_at,deleted)
         values (%s,%s,%s,%s,%s,%s,%s)
        """
        curs.execute(sql, (title, content, content_image, user_id, created_at, updated_at,deleted))

        db.commit()
        db.close()

        return redirect("/")












@app.route('/logout')
def logout():
    session.pop("name")
    return redirect("/")


#write 글쓰기 페이지

@app.route('/write')
def write():
    return render_template('write.html')

    #
    # if "name" in session:
    #     return render_template('write.html', name = session.get("name"), login = True)
    # else:
    #     return render_template('write.html', login = False)



@app.route('/post')
def post():
    return render_template('post.html')


@app.route('/posting', methods=['GET'])
def get_posting():
    print('get_posting')
    db = pymysql.connect(host='localhost', user='root', db='i_log', password='abc1234', charset='utf8')
    curs = db.cursor()

    sql = """
    SELECT *
    FROM post as p
    LEFT JOIN `user` as u
    ON p.user_id = u.id
    """

    # sql = """
    #  SELECT *
    #  FROM `user` as u
    #  LEFT JOIN `group` as g
    #    ON u.group_id = g.id
    #   """
    curs.execute(sql)

    rows = curs.fetchall()
    print(rows)

    json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
    db.commit()
    db.close()
    return json_str, 200










# 서버실행
if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 5000, debug = True)
