import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import datetime
import pymongo

client = pymongo.MongoClient(host='127.0.0.1', port=27017, tz_aware=False)
db = client.test


def save_data(log_data):
    """ 保存到mongo db"""
    wq_access = db.wq_access
    for log in log_data[::-1]:
        data = {
            "log": log,
            "create_date": datetime.datetime.now()
        }
        wq_access.insert(data)


def get_last_log():
    """ 获取最新的日志信息"""
    wq_access = db.wq_access
    last_log = wq_access.find({}).sort("create_date", -1).limit(1)
    log = None
    for i in list(last_log):
        log = i['log']

    return log


def get_log(log_path):
    """获取日志内容"""
    data_list = []

    last_log = get_last_log()
    with open(log_path, 'r') as file:
        lines = file.readlines()
        for line in lines[::-1]:
            sentence = line.split('\n')[0]
            if sentence == last_log:
                break
            data_list.append(sentence)
            if last_log is None and len(data_list) == 100:
                break
    save_data(data_list)


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_modified(self, event):
        if not event.is_directory:
            path = os.path.realpath(event.src_path)
            get_log(path)


if __name__ == "__main__":
    path = '/Users/xufengxu/tem_data/logs'
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()