import datetime

from bson import ObjectId


def mongo_wrap(mongo_cursor):
    """ 对mongo db 的数据进行包装下"""

    tem_data = []
    for item in mongo_cursor:
        item['create_date'] = item['create_date'].strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(item['_id'], ObjectId):
            item['_id'] = str(item['_id'])

        tem_data.append(item)
    return tem_data


def get_data_by_conditions(start, end, key_words, collection):
    """ 根据筛选条件获取日志数据"""

    conditions = {}
    create_date_dict = {}
    if start:
        start_time = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        create_date_dict["$gt"] = start_time

    if end:
        end_time = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        create_date_dict["$lt"] = end_time

    if key_words:
        conditions['log'] = {"$regex": key_words}

    if start or end:
        conditions['create_date'] = create_date_dict

    data = collection.find(conditions).sort("create_date", -1).limit(500)
    return data
