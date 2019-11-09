# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from search.items import SearchItem, ReplyItem
import pymongo


class SearchPipeline(object):
    def __init__(self):
        # 初始化数据库
        db_name = "weibo"
        # TODO: 数据库地址
        host = "www.***.com"
        # TODO：数据库端口号
        port = 27017
        client = pymongo.MongoClient(host=host, port=port)
        db = client.admin
        # TODO: 数据库登录账号密码
        db.authenticate("**", "****", mechanism="SCRAM-SHA-1")
        self.my_db = client[db_name]

    def process_item(self, item, spider):
        # print(item)
        data = dict(item)
        if isinstance(item, SearchItem):
            # print("微博内容")
            d = self.my_db.content.find_one({"mid": data['mid']})
            if d is None:
                self.my_db.content.insert_one(data)
        elif isinstance(item, ReplyItem):
            # if "root_reply_id" in item and item['root_reply_id'] is not None:
            #     print("二级回复")
            # else:
            #     print("一级回复")
            d = self.my_db.reply.find_one({"reply_id": data['reply_id']})
            if d is None:
                self.my_db.reply.insert_one(data)
        else:
            print("invalid data -")
            pass
        return item
