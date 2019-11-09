import pymongo, requests, os, math, time
from threading import Thread

db_name = "weibo"
# TODO: 数据库地址
host = "www.*****.com"
# TODO：数据库端口号
port = 27017
client = pymongo.MongoClient(host=host, port=port)
db = client.admin
# TODO: 数据库登录账号密码
db.authenticate("**", "****", mechanism="SCRAM-SHA-1")
my_db = client[db_name]

download_num = 0


def download_image(url, file_name, download_num):
    try:
        if not os.path.exists("./image"):
            os.makedirs("./image")
        res = requests.get(url)
        img = res.content
        file_path = "./image/" + file_name
        file_writer = open(file_path, 'wb')
        file_writer.write(img)
        print(url, "下载完成", download_num)
    except:
        print("download error")


data_list = my_db.reply_backup.find({"img_url": {"$ne": None}})
for item in data_list:
    # item["img_url"].replace("thumb180", "")]
    str_list = item["img_url"].split("/")
    str_list[3] = "large"
    file_name = str_list[4]
    url = "/".join(str_list)
    download_num += 1
    download_image(url=url, file_name=file_name, download_num=download_num)

# data_list = list(my_db.content.find({"user_pics": {"$ne": None}}))
# length = my_db.content.count_documents({"user_pics": {"$ne": None}})
# reply_list = list(my_db.reply.find({}))
# print(len(reply_list))
# count = 0
# for item in reply_list:
#     count += 1
#     d = list(my_db.reply.find({"reply_id": item['reply_id']}))
#     if 1 < len(d):
#         print(len(d), item["reply_id"])
# d = my_db.reply.find_one({"reply_id": "4369216980668210"})
# print(d)

# my_db.reply_backup.insert_many(reply_list)


# class Download(Thread):
#     def __init__(self, item_list):
#         super().__init__()
#         self.item_list = item_list
#
#     def run(self):
#         try:
#             for item in self.item_list:
#                 for url in item['user_pics']:
#                     str_list = url.split("/")
#                     str_list[3] = "large"
#                     file_name = item["user_name"] + "_____" + str_list[4]
#                     _url = "/".join(str_list)
#                     self.download_image(url=_url, file_name=file_name)
#         except:
#             print("for error")
#
#     def download_image(self, url, file_name):
#         try:
#             if not os.path.exists("./image/s"):
#                 os.makedirs("./image/s")
#             res = requests.get(url)
#             img = res.content
#             file_path = "./image/s/" + file_name
#             file_writer = open(file_path, 'wb')
#             file_writer.write(img)
#             print(url, "下载完成")
#         except:
#             print("download error")
#
#
# item_list_run = []
#
# x = 100
#
# for i in range(math.ceil(length / x)):
#     try:
#         start = i * x
#         end = start + x if start + x < length else length
#         item_list = data_list[start:end]
#         item = Download(item_list)
#         item.start()
#         print("i :", i)
#     except:
#         print("create error")
