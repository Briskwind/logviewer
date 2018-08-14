import datetime
import pymongo

client = pymongo.MongoClient(host='127.0.0.1', port=27017, tz_aware=False)

db = client.test
collection = db.wq_access

# 使用新 collection 会自动创建
# new_collection = db.new_collection
# data = {
#     "name": 'name'
# }
# new_collection.insert(data)

# 增
# collection.insert(data)

# 删
# res = collection.remove()


# 按条件更新，添加为空则是所有数据
# res = collection.update({'index': {"$gt": 30, "$lt": 35}}, {'$set': {'name': 'real_name'}}, multi=True)



# 范围查找
# res = collection.find({}).sort("create_date", -1).limit(5)
# for i in list(res):
#     print(i['log'])
#     print(i['create_date'].strftime('%Y-%m-%d %H:%M:%S'))
# 模糊查询
# data2 = collection.find({"name":{"$regex":"real"}})
# print('data2', list(data2))



import time

a = "2011-09-28 10:00:00"

date_time = datetime.datetime.strptime(a,'%Y-%m-%d %H:%M:%S')
print('date_time', type(date_time))


