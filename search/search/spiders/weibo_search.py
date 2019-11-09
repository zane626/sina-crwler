# -*- coding: utf-8 -*-
import scrapy, json, re, time
from scrapy.http import Request
from search.utils.utils import get_search_url, get_pics, get_reply_url, get_sub_reply_url
from scrapy.loader import ItemLoader
from search.items import SearchItem, ReplyItem


class WeiboSearchSpider(scrapy.Spider):
    name = 'weibo_search'

    # def make_requests_from_url(self, url):
    #     return Request(url, dont_filter=True)
    def __init__(self, keyword, reply=False, *args, **kwargs):
        super(WeiboSearchSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.page = 0
        self.is_get_reply = reply

    def start_requests(self):
        self.page += 1
        # url = get_search_url(keyword=self.keyword, page=self.page)
        # yield Request(url, callback=self.parse)
        url = get_reply_url("4367970740108457")
        yield Request(url=url, callback=self.parse_reply, meta={
            "id_str": "4367970740108457"
        })

    def parse(self, response):
        data = json.loads(str(response.text))
        if 1 == data['ok']:
            card_list = data['data']['cards']
            for item in card_list:
                if "card_type_name" in item and "微博" == item["card_type_name"]:
                    _data = self.__get_blog(item)
                    data_item = ItemLoader(item=SearchItem(), response=response)
                    data_item.add_value("user_name", _data['user_name'])
                    data_item.add_value("user_id", _data['user_id'])
                    data_item.add_value("user_verified_reason", _data['user_verified_reason'])
                    data_item.add_value("user_description", _data['user_description'])
                    data_item.add_value("user_followers_count", _data['user_followers_count'])
                    data_item.add_value("user_statuses_count", _data['user_statuses_count'])
                    data_item.add_value("reposts_count", _data['reposts_count'])
                    data_item.add_value("comments_count", _data['comments_count'])
                    data_item.add_value("attitudes_count", _data['attitudes_count'])
                    data_item.add_value("user_content", _data['user_content'])
                    data_item.add_value("created_at", _data['created_at'])
                    data_item.add_value("source", _data['source'])
                    data_item.add_value("mid", _data['mid'])
                    data_item.add_value("idstr", _data['idstr'])
                    data_item.add_value("user_pics", _data['user_pics'])
                    yield data_item.load_item()
                    # 是否爬去回复
                    if self.is_get_reply:
                        reply_first_url = get_reply_url(id_str=_data['idstr'])
                        meta = {
                            "idstr": _data["idstr"],
                            "url": reply_first_url
                        }
                        yield Request(url=reply_first_url, callback=self.parse_reply, meta=meta)
                else:
                    if "card_group" in item:
                        for it in item["card_group"]:
                            if "mblog" in it:
                                _data = self.__get_blog(it)
                                data_item = ItemLoader(item=SearchItem(), response=response)
                                data_item.add_value("user_name", _data['user_name'])
                                data_item.add_value("user_id", _data['user_id'])
                                data_item.add_value("user_verified_reason", _data['user_verified_reason'])
                                data_item.add_value("user_description", _data['user_description'])
                                data_item.add_value("user_followers_count", _data['user_followers_count'])
                                data_item.add_value("user_statuses_count", _data['user_statuses_count'])
                                data_item.add_value("reposts_count", _data['reposts_count'])
                                data_item.add_value("comments_count", _data['comments_count'])
                                data_item.add_value("attitudes_count", _data['attitudes_count'])
                                data_item.add_value("user_content", _data['user_content'])
                                data_item.add_value("created_at", _data['created_at'])
                                data_item.add_value("source", _data['source'])
                                data_item.add_value("mid", _data['mid'])
                                data_item.add_value("idstr", _data['idstr'])
                                data_item.add_value("user_pics", _data['user_pics'])
                                yield data_item.load_item()
                                # 是否爬去回复
                                if self.is_get_reply:
                                    reply_first_url = get_reply_url(id_str=_data['idstr'])
                                    meta = {
                                        "idstr": _data["idstr"],
                                        "url": reply_first_url
                                    }
                                    yield Request(url=reply_first_url, callback=self.parse_reply, meta=meta)
                            else:
                                # print("no_1_data")
                                pass
                    else:
                        # print("no_data")
                        pass
        else:
            print("content interface error, ", "\n", data["msg"])
        if 1 > self.page:
            self.page += 1
            next_url = get_search_url(keyword=self.keyword, page=self.page)
            yield Request(next_url, callback=self.parse)

    # 提取数据
    @staticmethod
    def __get_blog(item) -> dict:
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
            data["user_pics"] = get_pics(item['mblog']['pics'])
        else:
            data['user_pics'] = []
        return data

    def parse_reply(self, response):
        id_str = response.meta['id_str']
        try:
            back_data = json.loads(str(response.text))
            if "data" not in back_data:
                print("no 'data' key", back_data, response.url)
                return
        except:
            if "timeout_retry" in response.meta:
                timeout_retry = response.meta['timeout_retry']
            else:
                timeout_retry = 0
            if 11 > timeout_retry:
                timeout_retry += 1
                print("the data returned from interface is not expected", timeout_retry)
                yield Request(url=response.url, callback=self.parse_reply, meta={
                    "id_str": id_str,
                    "timeout_retry": timeout_retry
                })
            else:
                print("Too many retries. Don't try again", response.url)
            back_data = None
        if back_data is None:
            return
        try:
            if "data" in back_data['data']:
                data_list = back_data['data']['data']
            else:
                data_list = back_data['data']
            for item in data_list:
                data = ItemLoader(item=ReplyItem(), response=response)
                try:
                    data.add_value("user_reply", item['text'])
                    data.add_value("user_name", item['user']['screen_name'])
                    data.add_value("user_id", item['user']['id'])
                    data.add_value("created_at", item['created_at'])
                    data.add_value("idstr", id_str)
                    data.add_value("reply_id", item['mid'])
                    data.add_value("fetchTime", int(time.time() * 1000))
                    data.add_value("root_reply_id", None if item['mid'] == item['rootidstr'] else item['rootidstr'])
                    data.add_value("img_url", item['pic']['large']['url'] if "pic" in item else "")
                    data.add_value("user_verified_reason",
                                   item['user']['verified_reason'] if "verified_reason" in item["user"] else "")
                    data.add_value("user_description", item['user']['description'])
                    data.add_value("user_followers_count", item['user']['followers_count'])
                    data.add_value("user_statuses_count", item['user']['statuses_count'])
                    data.add_value("comments_count", item['total_number'] if "total_number" in item else 0)
                    data.add_value("attitudes_count", item['like_count'])
                    yield data.load_item()
                    if "total_number" in item and 0 != item['total_number']:
                        sub_reply_url = get_sub_reply_url(mid=item['mid'])
                        yield Request(url=sub_reply_url, callback=self.parse_sub_reply, meta={
                            "id_str": id_str,
                            "mid": item['mid']
                        })
                except Exception as err:
                    print("get data err--->", err)

            if "data" in back_data['data']:
                max_id = back_data['data']['max_id']
                max_id_type = back_data['data']['max_id_type']
            else:
                max_id = back_data['max_id']
                max_id_type = back_data['max_id_type']
            # max_id 等于0 代表没有下一页
            if 0 != max_id:
                next_url = get_reply_url(id_str=id_str, max_id_type=max_id_type, max_id=max_id)
                yield Request(url=next_url, callback=self.parse_reply, meta=response.meta)
        except Exception as err:
            print("err---->", err)

    def parse_sub_reply(self, response):
        id_str = response.meta['id_str']
        mid = response.meta['mid']
        try:
            back_data = json.loads(str(response.text))
        except:
            print("json error", response.text)
            back_data = None
        if back_data is None:
            return
        if "data" in back_data['data']:
            data_list = back_data['data']['data']
        else:
            data_list = back_data['data']
        for item in data_list:
            data = ItemLoader(item=ReplyItem(), response=response)
            data.add_value("user_reply", item['text'])
            data.add_value("user_name", item['user']['screen_name'])
            data.add_value("user_id", item['user']['id'])
            data.add_value("created_at", item['created_at'])
            data.add_value("idstr", id_str)
            data.add_value("reply_id", item['mid'])
            data.add_value("fetchTime", int(time.time() * 1000))
            data.add_value("root_reply_id", None if item['mid'] == item['rootidstr'] else item['rootidstr'])
            data.add_value("img_url", item['pic']['large']['url'] if "pic" in item else None)
            data.add_value("user_verified_reason",
                           item['user']['verified_reason'] if "verified_reason" in item["user"] else None)
            data.add_value("user_description", item['user']['description'])
            data.add_value("user_followers_count", item['user']['followers_count'])
            data.add_value("user_statuses_count", item['user']['statuses_count'])
            data.add_value("comments_count", 0)
            data.add_value("attitudes_count", item['like_count'])
            yield data.load_item()
        try:
            max_id = back_data['max_id']
            max_id_type = back_data['max_id_type']
            # max_id 等于0 代表没有下一页
            if 0 != max_id:
                next_url = get_sub_reply_url(mid=mid, max_id_type=max_id_type, max_id=max_id)
                yield Request(url=next_url, callback=self.parse_reply, meta=response.meta)
        except Exception as err:
            print("err--->", err)
