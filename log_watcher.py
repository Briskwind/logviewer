import os, sys
import time
import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "logviewer.settings")
import django

django.setup()

from logviewer.settings import WATCH_PATH
from extensions.mongo_conf import db, ACCESS, NGINX_ACCESS, DRUGLISTRPC_OUT, WANGQIANCELERY_ERR
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def save_data(log_data, collection):
    """ 保存到mongo db"""
    for log in log_data[::-1]:
        data = {
            "log": log,
            "create_date": datetime.datetime.now()
        }
        collection.insert(data)


def get_last_log(collection):
    """ 获取最新的日志信息"""

    last_log = collection.find({}).sort("create_date", -1).limit(1)
    log = None
    for i in list(last_log):
        log = i['log']

    return log


def deal_log_file(log_path):
    """获取某个日志内容"""
    log_name = log_path.split('/')[-1]

    if log_name == 'access.log':
        collection = ACCESS
    elif log_name == 'wangqian_access.log':
        collection = NGINX_ACCESS
    elif log_name == 'druglistrpc-out-2.log':
        collection = DRUGLISTRPC_OUT
    elif log_name == 'wangqiancelery.err.log':
        collection = WANGQIANCELERY_ERR
    else:
        collection = db.default

    data_list = []
    last_log = get_last_log(collection)
    with open(log_path, 'r') as file:
        lines = file.readlines()
        for line in lines[::-1]:
            sentence = line.split('\n')[0]
            if sentence == last_log:
                break
            data_list.append(sentence)
            if last_log is None and len(data_list) == 100:
                break
    save_data(data_list, collection)


class FileEventHandler(FileSystemEventHandler):
    """ 监听文件改变"""

    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_modified(self, event):
        if not event.is_directory:
            path = os.path.realpath(event.src_path)
            deal_log_file(path)


if __name__ == "__main__":
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_PATH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


