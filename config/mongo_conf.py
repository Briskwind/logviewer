import datetime
import json

import pymongo
from bson import ObjectId

from logviewer.settings import MONGO_HOST, MONGO_PORT

client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT, tz_aware=False)


def mongo_wrap(mongo_cursor):
    tem_data = []
    for item in mongo_cursor:
        item['create_date'] = item['create_date'].strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(item['_id'], ObjectId):
            item['_id'] = str(item['_id'])

        tem_data.append(item)
    return tem_data
