import random, time
from urllib import parse
from search.utils.agent import user_agent


# 获取搜索url
def get_search_url(keyword, page) -> str:
    values = {
        "containerid": "100103type=1&q=" + keyword,
        "luicode": "10000011",
        "isnewpage": "1",
        "lfid": "106003type=1",
        "title": keyword,
        "page": page,
        "page_type": "searchall"
    }
    req_parse = parse.urlencode(values)
    url = "https://m.weibo.cn/api/container/getIndex?" + req_parse
    return url


# 获取带 user-agent header
def get_header() -> dict:
    return {"User-Agent": random.choice(user_agent)}


# 获取cookie
def get_cookies() -> dict:
    cookie = ""
    arr = cookie.split("; ")
    cookies = dict()
    for item in arr:
        a = item.split("=")
        cookies[a[0]] = a[1]
    return cookies


# 获取微博配图url
def get_pics(url_list) -> list:
    if url_list is not None and isinstance(url_list, list):
        pics = []
        for item in url_list:
            pics.append(item['large']['url'])
        return pics
    else:
        return []


# 获取评论url
def get_reply_url(id_str, max_id_type=0, max_id=None) -> str:
    max_id_str = ""
    if max_id is not None:
        max_id_str = "&max_id=" + str(max_id)
    return "https://m.weibo.cn/comments/hotflow?id=%s&mid=%s%s&max_id_type=%d" % (
        id_str, id_str, max_id_str, max_id_type)


# 获取二级评论url
def get_sub_reply_url(mid, max_id=None, max_id_type=0) -> str:
    max_id_str = ""
    if max_id is not None:
        max_id_str = "&max_id=" + str(max_id)
    return "https://m.weibo.cn/comments/hotFlowChild?cid=%s%s&max_id_type=%d" % (mid, max_id_str, max_id_type)
