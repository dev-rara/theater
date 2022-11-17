import requests
from pymongo import MongoClient
client = MongoClient('보안상 삭제')
db = client.theater

url = 'http://openapi.seoul.go.kr:8088/개인키 보안상 삭제/json/culturalEventInfo/1/100/ /'
response = requests.get(url).json()
theater_list = (response['culturalEventInfo']['row'])
# print(theater_list)

id = 0
for list in theater_list :
    # print (list)
    id += 1
    doc = {
        'TITLE' : list['TITLE'],
        'DATE': list['DATE'],
        'PLACE': list['PLACE'],
        'ORG_LINK': list['ORG_LINK'],
        'MAIN_IMG': list['MAIN_IMG'],
        'CODENAME': list['CODENAME'],
        'PROGRAM': list['PROGRAM'],
        'theater_id': id
    }
    # print(doc)
    # db.theater_list.insert_one(doc)

