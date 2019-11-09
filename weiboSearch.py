import requests, json, re, pymongo, config
from time import sleep
from index import run_reply


class Search:
    def __init__(self, key_word=None):
        self.keyword = key_word
        self.page = 0
        self.can_continue = True
        # 初始化数据库
        db_name = "weibo"
        # TODO: 数据库地址
        host = ""
        # TODO: 数据库端口号
        port = 27017
        client = pymongo.MongoClient(host=host, port=port)
        db = client.admin
        # TODO: 数据库账号密码
        db.authenticate("**", "***", mechanism="SCRAM-SHA-1")
        self.my_db = client[db_name]
        self.is_get_reply = False
        self.count = 0

    def run(self):
        while self.can_continue:
            self.page += 1
            url = config.get_search_url(self.keyword, page=self.page)
            self.__req(url=url, cookies=config.cookies)
            # 3秒获取一次新页面
            sleep(3)

    # 请求
    def __req(self, url, cookies=None):
        try:
            res_pones = requests.get(url, headers=config.get_header(), cookies=cookies)
            data = json.loads(str(res_pones.text))
            if 1 == data['ok']:
                card_list = data['data']['cards']
                self.__processing_data(card_list)
            else:
                print("获取结束, 接口数据异常, 页数:", self.page, "\n", data["msg"])
                self.can_continue = False
        except Exception as err:
            print("获取结束, 方法执行异常, 页数:", self.page, "\n", err)
            self.can_continue = False

    # 处理数据
    def __processing_data(self, card_list):
        for item in card_list:
            if "card_type_name" in item and "微博" == item["card_type_name"]:
                data = self.__get_blog(item)
                self.count += 1
                print("insert", data["user_name"], self.count)
                self.my_db.content.insert_one(data)
            else:
                if "card_group" in item:
                    for it in item["card_group"]:
                        if "mblog" in it:
                            data = self.__get_blog(it)
                            self.count += 1
                            print("insert", data["user_name"], self.count)
                            self.my_db.content.insert_one(data)
                        else:
                            # print("no_1_data")
                            pass
                else:
                    # print("no_data")
                    pass

    # 提取数据
    def __get_blog(self, item) -> dict:
        data = dict()
        # 用户姓名
        data["user_name"] = item['mblog']['user']['screen_name']
        # 用户id
        data["user_id"] = item['mblog']['user']['id']
        # 用户认证
        if "verified_reason" in item['mblog']["user"]:
            data["user_verified_reason"] = item['mblog']['user']['verified_reason']
        else:
            data["user_verified_reason"] = None
        # 用户描述
        data["user_description"] = item['mblog']['user']['description']
        # 粉丝
        data["user_followers_count"] = item['mblog']['user']['followers_count']
        # 发布微博数量
        data["user_statuses_count"] = item['mblog']['user']['statuses_count']
        # 此条转发数
        data['reposts_count'] = item['mblog']['reposts_count']
        # 此条评论数
        data["comments_count"] = item['mblog']['comments_count']
        # 此条点赞
        data['attitudes_count'] = item['mblog']['attitudes_count']
        # 微博内容
        if "longText" in item['mblog'] and "longTextContent" in item['mblog']["longText"]:
            data["user_content"] = item['mblog']['longText']['longTextContent'].strip()
        elif "raw_text" in item['mblog']:
            data["user_content"] = item['mblog']["raw_text"]
        else:
            html_re = re.compile(r"<.+?>")
            data["user_content"] = html_re.sub("", item['mblog']["text"]).strip()
        # 时间
        data["created_at"] = item['mblog']['created_at']
        # 来源
        data['source'] = item['mblog']['source']
        # d据传是最原始的微博id，据传已废除；
        # mid是单条微博的id，通过接口可使用mid进行大部分操作；
        # idstr：所有涉及回复的接口（非评论），都应使用idstr
        # 微博id
        data['id'] = item['mblog']['id']
        data['mid'] = item['mblog']['mid']
        data['idstr'] = item['mblog']['idstr']
        # 配图
        if "pics" in item['mblog']:
            data["user_pics"] = self.__get_pics(item['mblog']['pics'])
        # 是否爬去回复
        if self.is_get_reply:
            run_reply(id_str=data['idstr'])
        return data

    # 获取微博配图url
    def __get_pics(self, url_list) -> list:
        if url_list is not None and isinstance(url_list, list):
            pics = []
            for item in url_list:
                pics.append(item['large']['url'])
            return pics
        else:
            return []
