import datetime
import pymongo

client = pymongo.MongoClient(host='127.0.0.1', port=27017, tz_aware=False)



def mongo_wrap(mongo_cursor):
    tem_data = []
    for item in mongo_cursor:
        item['create_date'] = item['create_date'].strftime('%Y-%m-%d %H:%M:%S')
        tem_data.append(item)
    return tem_data




