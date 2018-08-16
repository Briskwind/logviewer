
import pymongo

from logviewer.settings import MONGO_HOST, MONGO_PORT

client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT, tz_aware=False)

# 日志存储数据库
db = client.logs

# 网签 access.log
ACCESS = db.access

# nginx 日志用于测试
NGINX_ACCESS = db.wangqian_access

# druglistrpc
DRUGLISTRPC_OUT = db.druglistrpc_out
DRUGLISTRPC_ERROR = db.druglistrpc_error


# 网签celery
WANGQIANCELERY_ERR = db.wangqiancelery_err