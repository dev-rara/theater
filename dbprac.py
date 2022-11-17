from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.aphlzi8.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


# 저장 - 예시
doc = {'name':'bobby','age':21}
db.users.insert_one(doc)

# 한 개 찾기 - 예시
user = db.users.find_one({'name':'bobby'})

# 여러개 찾기 - 예시 ( _id 값은 제외하고 출력, 조건없음, 위에거 조건)
all_users = list(db.users.find({},{'_id':False}))

# 바꾸기 - 예시
db.users.update_one({'name':'bobby'},{'$set':{'age':19}})

# 지우기 - 예시
db.users.delete_one({'name':'bobby'})

# 컬렉션 개수 얻기 - 예시
db.users.countDocuments(Query, Options)
db.users.count_document({ 'key' : value })
collection.estimated_document_count()
# MongoDB에서 countDocuments() 메서드는 선택 기준과 일치하는 문서 수를 계산합니다.
# 선택 기준과 일치하는 문서의 총 수를 나타내는 숫자 값을 반환합니다.
# 첫 번째는 선택 기준이고 다른 하나는 선택 사항입니다.

# 특정 단어가 들어간 데이터 검색: $regex
db.collection.find({ 'content': {'$regex': '안녕'} })

# title과 content 모두에 특정단어가 들어간 데이터 검색: $and + $regex
db.collection.find({'$and': [ {'title':{'$regex':'안녕'}},{'content':{'$regex':'안녕'}} ]})