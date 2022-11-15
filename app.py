from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
import certifi
import jwt
import datetime
import hashlib

ca = certifi.where()
client = MongoClient('mongodb+srv://user01:sparta@cluster0.noigl81.mongodb.net/?retryWrites=true&w=majority')
db = client.theater

app = Flask(__name__)

SECRET_KEY = 'SPARTA'

# HTML을 주는 부분
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({'id': payload['id']})
        return render_template('login.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg='로그인 시간이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg='로그인 정보가 존재하지 않습니다.'))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/signup')
def register():
    return render_template('register.html')

### 개발단계 로그인 성공 테스트용
@app.route('/index')
def index():
    return render_template('index.html')


# API
@app.route('/api/signup', methods=['POST'])
def sign_up():
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    
    doc = {
        'id': id_receive,
        'password': pw_hash,
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/api/signup/check-id', methods=['POST'])
def check_dup():
    id_receive = request.form['id_give']
    exists = bool(db.users.find_one({'id': id_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/api/login', methods=['POST'])
def sign_in():
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': id_receive, 'password': pw_hash})
    
    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)