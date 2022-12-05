from flask import Flask, render_template

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

# 서버실행
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)

