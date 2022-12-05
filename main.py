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


# 서버실행
if __name__ == '__main__':
    app.run('0.0.0.0', port = 5000, debug = True)
