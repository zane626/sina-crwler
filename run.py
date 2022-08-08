import time
import random
from weiboHotList import Hot

last_time = time.time()


def get_m(t) -> int:
    return int(time.strftime('%M', time.localtime(t)))


def get_r() -> int:
    return random.sample(range(0, 11), 1)[0]


def log(s):
    file_name = 'run.log'
    with open(file_name, 'w')as file:
        file.write(s)


while True:
    if get_m(last_time) != get_m(time.time()):
        last_time = time.time()
        Hot(now_time=int(last_time), log=log).run()
    else:
        time.sleep(get_r())
