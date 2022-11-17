from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
import certifi
import jwt
import datetime
import hashlib
import requests
from bson.json_util import dumps



ca = certifi.where()
# client = MongoClient('mongodb+srv://user01:sparta@cluster0.noigl81.mongodb.net/?retryWrites=true&w=majority')
client = MongoClient('mongodb+srv://test:sparta@cluster0.aphlzi8.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.theater

app = Flask(__name__)

SECRET_KEY = 'SPARTA'


# HTML 화면 렌더링
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'id': payload['id']})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg='로그인 시간이 만료되었습니다.'))
    except jwt.exceptions.DecodeError:
        return redirect(url_for('login', msg='로그인 정보가 존재하지 않습니다.'))

# 로그인 페이지
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

# 회원가입 페이지
@app.route('/signup')
def register():
    return render_template('register.html')


# 상세페이지
@app.route('/detail/<id>')
def detail(id):
    # id(공연)로 DB에서 데이터를 가지고 온다.
    # 렌더 부분에 진자템플릿으로 내용을 준다.
    token_receive = request.cookies.get('mytoken')
    print(id)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({'id': payload['id']})
        theater = db.theater_list.find_one({"theater_id": int(id)}, {"_id": False})
        # review = db.review.find_one({"theater_id": int(id)}, {"_id": False})
        print(theater, '선택')
        return render_template('detail.html', theater=theater, user_info=user_info )
    except:
        return redirect(url_for("home"))





# 마이페이지
@app.route('/mypage/<user>')
def mypage(user):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # jinja를 사용해 html에 status의 값을 넘겨준다
        status = (user == payload["id"])
        user_info = db.users.find_one({"id": user}, {"_id": False})
        # print(user_info, '유저정보')
        return render_template('mypage.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

    # return render_template('mypage.html')




# API 기능
# 회원가입
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


# 회원가입 - 아이디중복체크
@app.route('/api/signup/check-id', methods=['POST'])
def check_dup():
    id_receive = request.form['id_give']
    exists = bool(db.users.find_one({'id': id_receive}))
    return jsonify({'result': 'success', 'exists': exists})

# 로그인
@app.route('/api/login', methods=['POST'])
def sign_in():
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': id_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 공연 전체 list
@app.route("/theater", methods=["GET"])
def theater_show():
    type_receive = request.args.get('type_give')
    theater_list = list(db.theater_list.find({'CODENAME':{'$regex':type_receive}}))
    # print(theater_list)
    # DB조건 추가시 CODENAME, 파일 타입 에러로 인한 import와 코드 추가
    return jsonify({'result': 'success', 'theater_list': dumps(theater_list)})


# 공연 검색 list
@app.route("/search", methods=["GET"])
def theater_search():
    codename_receive = request.args.get('codename')
    input_receive = request.args.get('input_query')
    # DB에 두가지 조건이 모두 만족하는 데이터를 찾을 때
    # search_result = list(db.theater_list.find({'$and': [{'CODENAME': {'$regex': codename_receive}}, {'TITLE': {'$regex': input_receive}}]}))
    search_result = list(db.theater_list.find({'TITLE':{'$regex':input_receive}}))

    # print(search_result)
    # DB조건 추가시 CODENAME, 파일 타입 에러로 인한 import와 코드 추가
    return jsonify({'result': 'success', 'search_result': dumps(search_result)})



# 메인에서 리뷰작성 버튼 클릭 -> 데이터포함 페이지 이동
@app.route("/detail", methods=["GET"])
def detail_page():
    id_receive = request.args.get('id_give')
    return jsonify({'result': 'success', 'url':id_receive})


# 디테일 페이지 - 리뷰저장
@app.route("/review", methods=["POST"])
def review_post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # DB값
        user_info = db.users.find_one({"id": payload["id"]})
        # 받아오는 값
        review_receive = request.form['review_give']
        id_receive = request.form['id_give']
        # print(user_info, review_receive,id_receive)

        doc = {
            'userid': user_info['id'],
            'review': review_receive,
            'theater_id': id_receive,
        }
        db.review.insert_one(doc)
        return jsonify({"result": "리뷰 DB저장", })

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        # 토큰 유효기간 만료, 토큰에러 났을 때 메인페이지로 이동
        return redirect(url_for("home"))


# 디테일 페이지 - 리뷰 보여줌
@app.route("/review", methods=["GET"])
def review_get():
    review_list = list(db.review.find({},{'_id':False}))
    # print(review_list)
    return jsonify({'review_list': review_list})


# 마이페이지 버튼 클릭 -> 데이터 포함 페이지 이동
@app.route("/myreview", methods=["GET"])
def myreview_page():
    return jsonify({'result': 'success'})


# 마이페이지 댓글 보여줌
@app.route("/mycard", methods=["GET"])
def myReviewShow():
    ID = request.args.get('id_give')
    review_list = list(db.review.find({'userid': {'$regex': ID}}))
    theater_list = list(db.theater_list.find({},{'_id':False}))
    # print(review_list,'리뷰정보')


    return jsonify({'review_list': dumps(review_list), 'theater_list': theater_list})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)