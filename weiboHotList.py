import config
import requests
import json
import pymongo
from account import db_name, host, port, name, pwd


class Hot:
    def __init__(self, now_time=None, log=None):
        client = pymongo.MongoClient(host=host, port=port, username=name, password=pwd)
        self.my_db = client[db_name]
        self.now_time = now_time
        self.log = log

    def run(self):
        self.__req(url=config.get_hot_list_url())

    def __req(self, url):
        try:
            header = config.get_header(lv=2)
            res_pones = requests.get(url, headers=header, cookies={})
            if 200 == res_pones.status_code:
                data = json.loads(str(res_pones.text))
                for item in data['data']['cards'][0]['card_group']:
                    item['created_at'] = self.now_time
                    self.my_db.hot_list.insert_one(item)
                    pass
            else:
                print("request error", res_pones.status_code)
                self.log("request error    " + str(res_pones.status_code) + "    " + self.now_time)
        except Exception as err:
            print("err1-->", err)
            self.log("err1-->    " + str(err) + "    " + self.now_time)
        pass


if __name__ == '__main__':
    Hot().run()
