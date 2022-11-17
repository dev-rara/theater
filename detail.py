<<<<<<< HEAD
# from flask import Flask, render_template, request, jsonify
# app = Flask(__name__)
#
# from pymongo import MongoClient
# client = MongoClient('mongodb+srv://test:test@cluster0.awecqav.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.dbsparta
#
# @app.route('/detail')
# def detail():
#     return render_template('detail.html')
#
# @app.route('/detail/post', methods=["POST"])
# def detail_post():
#     star_receive = request.form['star_give']
#     comment_receive = request.form['comment_give']
#     time_receive = request.form['time_give']
#
#
#     detail_list = list(db.details.find({}, {'_id': False}))
#     count = len(detail_list) + 1
#
#     doc = {
#         'time':time_receive,
#         'star':star_receive,
#         'comment':comment_receive,
#         'num': count
#     }
#     db.details.insert_one(doc)
#
#     return jsonify({'msg':'저장완료!'})
#
# @app.route('/detail/get', methods=["GET"])
# def detail_get():
#     detail_list = list(db.details.find({}, {'_id': False}))
#     return jsonify({'detail':detail_list})
#
# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5000, debug=True)
=======
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:test@cluster0.awecqav.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/detail/post', methods=["POST"])
def detail_post():
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    time_receive = request.form['time_give']


    detail_list = list(db.details.find({}, {'_id': False}))
    count = len(detail_list) + 1

    doc = {
        'time':time_receive,
        'star':star_receive,
        'comment':comment_receive,
        'num': count
    }
    db.details.insert_one(doc)

    return jsonify({'msg':'저장완료!'})

@app.route('/detail/get', methods=["GET"])
def detail_get():
    detail_list = list(db.details.find({}, {'_id': False}))
    return jsonify({'detail':detail_list})

# #공연 이미지, 내용 불러오기
# @app.route('/detail/information', methods=["GET"])
# def detail_get():
#     detail_list = list(db.details.find({}, {'_id': False}))
#     return jsonify({'detail':detail_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
>>>>>>> a3a4d782ef4dc368e45df7e13a30eae7895e5c08
