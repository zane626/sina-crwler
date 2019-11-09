from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options
import json

cookies_file_path = "./search/utils/cookies.txt"
account_file_path = "./search/utils/account"
driver_file_path = "./search/utils/chromedriver"


def get_account():
    f = open(cookies_file_path, "r+")
    f.truncate()
    f.close()
    account_list = []
    for line in open(account_file_path):
        li = line.strip().split(" ")
        account_list.append({
            "phone": li[0],
            "pwd": li[1]
        })
    for item in account_list:
        login_sina(phone=item['phone'], password=item['pwd'])


def login_sina(phone, password):
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(
        'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"')
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    try:
        driver = webdriver.Chrome(driver_file_path, chrome_options=chrome_options)
        try:
            driver.get("https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https://m.weibo.cn")
            sleep(5)
            account = driver.find_element_by_id("loginName")
            account.clear()
            account.send_keys(phone)
            pwd = driver.find_element_by_id("loginPassword")
            pwd.clear()
            pwd.send_keys(password)
            pwd.send_keys(Keys.RETURN)
            sleep(5)
            cookie_list = driver.get_cookies()
            cookie_obj = dict()
            for item in cookie_list:
                cookie_obj[item['name']] = item['value']
            f = open(cookies_file_path, 'a')
            f.write(json.dumps(cookie_obj) + '\n')
            f.close()
            driver.quit()
        except Exception as err:
            driver.quit()
            print("error1----->", err)

    except Exception as err:
        print("open brower error", err)
