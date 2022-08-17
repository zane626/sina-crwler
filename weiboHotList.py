import config
import requests
import json
import pymongo
from account import db_name, host, port, name, pwd
import pydash as _
import time


class Hot:
    def __init__(self, now_time=None, log=None, retry=0):
        client = pymongo.MongoClient(host=host, port=port, username=name, password=pwd)
        self.my_db = client[db_name]
        self.now_time = now_time
        self.log = log
        self.retry = retry

    def run(self):
        self.__req(url=config.get_hot_list_url())

    def __req(self, url):
        try:
            header = config.get_header(lv=2)
            res_pones = requests.get(url, headers=header, cookies={})
            if 200 == res_pones.status_code:
                data = json.loads(str(res_pones.text))
                group = _.get(data, 'data.cards[0].card_group', [])
                if len(group):
                    self.__extract(group)
                elif self.retry < 5:
                    self.run()
                else:
                    self.log('not data ----->   ' + str(res_pones.text), self.now_time)
            else:
                print("request error", res_pones.status_code)
                self.log("request error    " + str(res_pones.status_code) + "    " + self.now_time)
        except Exception as err:
            print("err1-->", err)
            self.log("err1-->    " + str(err) + "    " + self.now_time)
        pass

    def __extract(self, data):
        for item in data:
            item['created_at'] = self.now_time or int(time.time())
            self.my_db.hot_list.insert_one(item)
            pass


if __name__ == '__main__':
    Hot().run()
