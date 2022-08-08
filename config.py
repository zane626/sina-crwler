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
            "Cookie": "PC_TOKEN=d16fbf496a; SUB=_2AkMVsT63f8NxqwFRmP8RymvgbYpxzAHEieKj7c9sJRMxHRl-yj8XqmIstRB6PjEQWE5flyeYOcXZD5l78pHhv0lWBD7Z; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFgO_Lw35XIyizlRZNV-z2g"
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

def get_hot_list_url() -> str:
    params = {
        "containerid": "106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot",
        "title": "%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C",
        "extparam": "seat%3D1%26lcate%3D1001%26position%3D%257B%2522objectid%2522%253A%25228008631000000000000%2522%252C%2522name%2522%253A%2522%255Cu4e0a%255Cu6d77%255Cu5e02%2522%257D%26filter_type%3Drealtimehot%26pos%3D0_0%26c_type%3D30%26mi_cid%3D100103%26dgr%3D0%26recommend_tab%3D0%26cate%3D10103%26region_relas_conf%3D0%26display_time%3D1659943955%26pre_seqid%3D1639479645",
        "luicode": "10000011",
        "lfid": "231583"
    }
    par_str = []
    for key in params:
        par_str.append(key + '=' + params[key])
    return "https://m.weibo.cn/api/container/getIndex?" + ('&'.join(par_str))
