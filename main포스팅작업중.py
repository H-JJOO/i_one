from flask import Flask, render_template, request, session, redirect, flash, redirect, url_for
from werkzeug.utils import secure_filename
import pymysql
import os
import json
# import js2py
import bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "abcd"

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


##메인페이지에 찎어주자구
@app.route('/feed', methods=['GET'])
def get_posts():
    db = pymysql.connect(host='localhost', user='root', db='i_log', password='abc1234', charset='utf8')
    curs = db.cursor()

    sql = "select * from post"
    print(sql)

    curs.execute(sql)

    rows = curs.fetchall()
    print(rows)

    json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
    db.commit()
    db.close()
    return json_str, 200










# login
@app.route('/users/login', methods = ['GET', 'POST'])
def login():
    db = pymysql.connect(host = 'localhost', user = 'root', db = 'i_log', password = 'abc1234', charset = 'utf8')
    curs = db.cursor()

    if request.method == 'POST':
        uid = request.form['userId']
        upw = request.form['password']

        session['uid'] = request.form['userId']
        session['password'] = request.form['password']

        print(session)
        # print(session['uid'])

        # print(uid, upw)

        curs.execute("SELECT * FROM user")

        user_list = curs.fetchall()

        # print(user_list)

        for user in user_list:
            # print(user)
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
    print(session.get("uid"))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        content_image = request.form['content_image']
        user_id = session.get("uid")



        sql = """insert into post (title, content, content_image, user_id)
         values (%s,%s,%s,%s)
        """
        curs.execute(sql, (title, content, content_image, user_id))

        db.commit()
        db.close()

        return redirect("/")












@app.route('/logout')
def logout():
    session.pop("name")
    return redirect("/")


#write 글쓰기 페이지

# @app.route('/write')
# def write():
#     return render_template('write.html')

# write
@app.route('/write')
def write():
    return render_template('write.html', id = session.get("user"), name=session.get("name"), login=True)

    #
    # if "name" in session:
    #     return render_template('write.html', name = session.get("name"), login = True)
    # else:
    #     return render_template('write.html', login = False)



# @app.route('/post')
# def post():
#     return render_template('post.html')


# 테스트 하기 위한 포스팅페이지

@app.route('/posting')
def posting():
    return render_template('posting.html',  id = session.get("user"), name = session.get("name"), login = True)



@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        # 제출 요청한 파일이 있는지 확인
        if request.files['file'].filename == '':
            flash('파일이 없습니다. 파일을 제출하세요!')
            # 파일이 없으면 flash 전달. (현재 창에서 flash 메시지 출력.)
            return redirect(url_for('upload_file'))
        # if request.files['file'].filename == '':
        #    return '파일이 존재하지 않습니다.'

        # 파일이 존재한다면
        file = request.files['file']  # request.files: 단일 파일
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        # file.save(secure_filename(file.filename))
        # file.save(secure_filename(file.filename), 'static/uploads/' + secure_filename(file.filename))

        # file.filename: 업로드한 파일 이름
        # secure_filenmae: 파일이름을 보안 처리
        # file.save: 인자값으로 경로가 없으면 py파일과 같은 경로에 저장됨.
        return '파일 업로드 성공!!'



@app.route('/posting', methods=['GET', 'POST'])
def posting_uploader():

        db = pymysql.connect(host='localhost', user='root', db='i_log', password='Top1004top!', charset='utf8')
        curs = db.cursor()
        print("코드 도착")

        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            content_image = request.form['file']
            userid = session.get("uid")
            print(title, content)
            print("코드1도착")

            sql = """insert into post (title, content, content_image, userid)
                 values (%s,%s,%s,%s)
                """

            curs.execute(sql, (title, content, content_image, userid))

            db.commit()
            db.close()
            print("코드2도착")

        # 제출 요청한 파일이 있는지 확인
        if request.files['file'].filename == '':
            flash('파일이 없습니다. 파일을 제출하세요!')
            # 파일이 없으면 flash 전달. (현재 창에서 flash 메시지 출력.)
            print("코드3도착")
            return redirect(url_for('upload_file'))
        # if request.files['file'].filename == '':
        #    return '파일이 존재하지 않습니다.'

        # 파일이 존재한다면
        file = request.files['file']  # request.files: 단일 파일
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        # file.save(secure_filename(file.filename))
        # file.save(secure_filename(file.filename), 'static/uploads/' + secure_filename(file.filename))

        # file.filename: 업로드한 파일 이름
        # secure_filenmae: 파일이름을 보안 처리
        # file.save: 인자값으로 경로가 없으면 py파일과 같은 경로에 저장됨.
        return '파일 업로드 성공!!'







# 서버실행
if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 5000, debug = True)
