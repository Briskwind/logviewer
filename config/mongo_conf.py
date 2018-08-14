import datetime
import pymongo

from logviewer.settings import MONGO_HOST, MONGO_PORT

client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT, tz_aware=False)



def mongo_wrap(mongo_cursor):
    tem_data = []
    for item in mongo_cursor:
        item['create_date'] = item['create_date'].strftime('%Y-%m-%d %H:%M:%S')
        tem_data.append(item)
    return tem_data
