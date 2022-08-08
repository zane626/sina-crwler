# -*- coding: utf-8 -*-
import config
import requests
import json
import pymongo
import re
import time
from time import sleep
from pyquery import PyQuery as pq

s = requests.session()
s.keep_alive = False


class Reply:
    def __init__(self, id_str):
        self.id_str = id_str
        self.max_id = None
        self.can_continue = True
        # 初始化数据库
        db_name = "weibo"
        # TODO: 数据库地址
        host = "www.quandouyao.com"
        # TODO：数据库端口号
        port = 27017
        client = pymongo.MongoClient(host=host, port=port, username="root", password="zane2020")
        # client = pymongo.MongoClient(host=host, port=port)
        # db = client.admin
        # TODO: 数据库登录账号密码
        # db.authenticate("root", "zane2020", mechanism="SCRAM-SHA-1")
        self.my_db = client[db_name]
        self.count = 0
        self.sub_count = 0

    def run(self):
        self.__req(url=config.get_reply_url(id_str=self.id_str))

    def __req(self, url):
        try:
            header = config.get_header(lv=2)
            res_pones = requests.get(url, headers=header, cookies={})
            if 200 == res_pones.status_code:
                data = json.loads(str(res_pones.text))
                if "code" in data and "100000" == data['code']:
                    self.__layer(data['data']['html'])
                else:
                    print("interface error", data, self.count, self.sub_count)
            elif 404 == res_pones.status_code:
                self.__req(url=url)
            else:
                print("request error", res_pones.status_code)
        except Exception as err:
            print("err1-->", err, self.count, self.sub_count)
            self.can_continue = False

    def __layer(self, layer):
        try:
            try:
                pattern = re.compile(u'[\U00010000-\U0010ffff]')
            except re.error:
                pattern = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
            cont = pattern.sub('', layer)
            html = pq(cont.strip())
            try:
                next_url_params = pq(html('.list_ul>div')
                                     [-1:][0]).attr("action-data")
                if next_url_params is None:
                    next_url_params = pq(
                        html('.list_ul a')[-1:]).attr("action-data")
                if next_url_params is None:
                    next_url_params = ""
                    print("None", self.count, self.sub_count)
            except:
                next_url_params = ""
                print("no next url params", self.count, self.sub_count)
            for item in html('.list_box .list_ul .list_li').items():
                data = dict()
                text = item('.list_con .WB_text:first').html()
                text = re.findall(r"</a>：(.+)$", text)[0]
                pattern = re.compile('<(.|\n)+?>')
                # 回复内容
                data['user_reply'] = pattern.sub("", text).strip()
                # 用户昵称
                data['user_name'] = pq(item(".list_con .WB_text a")).html()
                # 用户ID
                data['user_id'] = pq(
                    item(".list_con .WB_text a")).attr('usercard')[2:]
                # 回复时间
                data['created_at'] = pq(item(".list_con .WB_from")).text()
                # 微博查回复ID
                data['idstr'] = self.id_str
                # 本条回复ID
                data['reply_id'] = pq(item).attr("comment_id")
                # 爬去时间
                data['fetchTime'] = int(time.time() * 1000)
                if 2 == pq(item(".list_box_in")).length:
                    data['sub_reply_content'] = re.findall(
                        r"(\d+)", pq(item(".list_box_in a:last")).text())[0]
                    # print("有二级回复", data['sub_reply_content'])
                    sub_url = pq(item(".list_box_in a:last")
                                 ).attr("action-data")
                    sleep(4)
                    self.__sub_reply_req(config.get_sub_reply_url(
                        sub_url), reply_sub_main_id=data['reply_id'])
                if 0 < len(pq(item)('.WB_media_wrap img')):
                    data['img_url'] = "https:" + \
                        pq(pq(item)('.WB_media_wrap img')[0]).attr("src")
                self.count += 1
                print(self.count, data)
                self.__save_data(data)
            sleep(3)
            if "" != next_url_params:
                next_url = "https://weibo.com/aj/v6/comment/big?ajwvr=6&from=singleWeiBo&__rnd=" + str(
                    int(time.time() * 1000)) + "&" + next_url_params
                return self.__req(url=next_url)
        except Exception as err:
            print("err2---->", err, self.count, self.sub_count)

    # 二级回复请求
    def __sub_reply_req(self, url, reply_sub_main_id):
        try:
            header = config.get_header(lv=2)
            res_pones = requests.get(url, headers=header)
            if 200 == res_pones.status_code:
                try:
                    data = json.loads(str(res_pones.text))
                    if "code" in data and "100000" == data['code']:
                        self.__sub_reply_parse(
                            data['data']['html'], reply_sub_main_id=reply_sub_main_id)
                    else:
                        print("sub interface error", data,
                              self.count, self.sub_count)
                except Exception as err:
                    print("json失败", err)
            elif 404 == res_pones.status_code:
                self.__sub_reply_req(
                    url=url, reply_sub_main_id=reply_sub_main_id)
            else:
                print("sub request error", res_pones.status_code,
                      self.count, self.sub_count)
        except Exception as err:
            print("err3---->", err, self.count, self.sub_count)
            self.can_continue = False

    # 二级回复解析
    def __sub_reply_parse(self, html_str, reply_sub_main_id):
        try:
            html = pq(html_str)
            try:
                next_url = pq(html(".list_li_v2 a")).attr("action-data")
            except:
                next_url = ""
            for item in pq(html(".list_li")).items():
                data = dict()
                try:
                    # 用户昵称
                    data["user_name"] = pq(
                        item(".list_con .WB_text a:first")).text()
                    # 用户ID
                    data["user_id"] = pq(
                        item(".list_con .WB_text a:first")).attr("usercard")[3:]
                    text = pq(item(".list_con .WB_text:first")).html()
                    text = re.findall(r"</a>：(.+)$", text)[0]
                    pattern = re.compile('<(.|\n)+?>')
                    # 回复
                    data["user_reply"] = pattern.sub("", text).strip()
                    data["created_at"] = pq(item(".WB_func .WB_from")).text()
                    data["idstr"] = self.id_str
                    data["reply_id"] = ""
                    data["reply_sub_id"] = pq(
                        item(".list_li")).attr("comment_id")
                    data["reply_sub_main_id"] = reply_sub_main_id
                    data['fetchTime'] = int(time.time() * 1000)
                    if 0 < pq(item(".WB_media_wrap")).length:
                        data['images'] = list()
                        for img in pq(item(".WB_media_wrap img")).items():
                            data["images"].append(
                                "https:" + pq(img).attr("src"))
                    self.sub_count += 1
                    self.__save_data(data)
                    # print("sub_count---->", self.sub_count)
                except Exception as err:
                    print("error5 数据提取错误---->", err, data)
            if next_url is not None and "" != next_url:
                sleep(3)
                self.__sub_reply_req(config.get_sub_reply_url(
                    next_url), reply_sub_main_id=reply_sub_main_id)
        except Exception as err:
            print("err4---->", err, self.count, self.sub_count)

    # 存储数据
    def __save_data(self, data):
        # print(self.count, self.sub_count)
        # print(data)
        self.my_db.reply.insert_one(data)
