db = {
    # 데이터베이스에 접속할 사용자 아이디
    'user': 'admin',
    # 사용자 비밀번호
    'password': 'ione1234',
    # 접속할 데이터베이스의 주소 (같은 컴퓨터에 있는 데이터베이스에 접속하기 때문에 localhost)
    'host': 'database-1.cbegjfm38p8o.ap-northeast-2.rds.amazonaws.com',
    # 관계형 데이터베이스는 주로 3306 포트를 통해 연결됨
    'port': 3306,
    # 실제 사용할 데이터베이스 이름
    'database': 'ione'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"