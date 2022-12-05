from flask import Flask, render_template

app = Flask(__name__)


# main
@app.route('/')
def root():
    return render_template('main.html')


# 서버실행
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000,debug=True)
