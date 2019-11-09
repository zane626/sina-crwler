import random, time
from urllib import parse
from useragent import useragent

cookies = {"_T_WM": "61002178017",
           "WEIBOCN_FROM": "1110006030",
           "MLOGIN": "0",
           "XSRF-TOKEN": "c1746d",
           "M_WEIBOCN_PARAMS": "featurecode%3D20000320%26luicode%3D10000011%26lfid%3D106003type%253D1%26fid%3D100103type%253D1%2526q%253D%25E5%25BE%25B7%25E5%259B%25BD%26uicode%3D10000011"}
'''
备注:
get_search_url:
    type: 搜索类型
        "1": "综合"
        "3": "用户"
        "61": "实时"
        "62": "关注"
        "64": "视频"
        "58": "问答"
        "21": "文章"
        "63": "图片"
        "87": "同城"
        "60": "热门"
        "38": "话题"
        "32": "主页"
'''


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
def get_header(lv=None) -> dict:
    if lv == 2:
        return {
            "User-Agent": random.choice(useragent),
            "Cookie": ""
        }
    else:
        return {"User-Agent": random.choice(useragent)}


# 获取评论url
def get_reply_url(id_str) -> str:
    time_str = str(int(time.time() * 1000))
    return "https://weibo.com/aj/v6/comment/big?ajwvr=6&id=%s&from=singleWeiBo&__rnd=%s" % (id_str, time_str)


# 获取二级评论url
def get_sub_reply_url(url):
    time_str = str(int(time.time() * 1000))
    return "https://weibo.com/aj/v6/comment/big?ajwvr=6" + url + (
            "&from=singleWeiBo&__rnd%s" % time_str) + "&display=0&retcode=6102"
