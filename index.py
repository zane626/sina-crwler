import weiboSearch
import weiboReply


def run_search(key_word):
    req = weiboSearch.Search(key_word=key_word)
    req.run()


def run_reply(id_str):
    req = weiboReply.Reply(id_str)
    req.run()


if __name__ == '__main__':
    # _key_word = "高考数学只考了124分"
    # run_search(key_word=_key_word)
    # 4367970740108457
    # 4415668650541468
    # 4411109769752589
    _id_str = "4367970740108457"
    run_reply(id_str=_id_str)
