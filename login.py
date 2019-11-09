from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.chrome.options import Options
import json


#
# try:
#     driver_url = "./chromedriver"
#     driver = webdriver.Chrome(driver_url, chrome_options=chrome_options)
#     try:
#         print("open website")
#         driver.get("https://weibo.com")
#         sleep(10)
#         print("ok ")
#         account = driver.find_element_by_id("loginname")
#         account.clear()
#         account.send_keys(account_list[0])
#         pwd = driver.find_element_by_name("password")
#         pwd.clear()
#         pwd.send_keys(account_list[1])
#         pwd.send_keys(Keys.RETURN)
#         print("enter")
#         sleep(10)
#         user_name = driver.find_element_by_class_name("gn_name").find_elements_by_tag_name("em")[1]
#         cookie_list = driver.get_cookies()
#         cookie = [item["name"] + "=" + item["value"] for item in cookie_list]
#         cookies = '; '.join(item for item in cookie)
#         f = open('cookies', 'a')
#         f.write(cookies + '\n')
#         driver.quit()
#     except Exception as err:
#         driver.quit()
#         print("error1----->", err)
#
# except Exception as err:
#     print("open brower error", err)


def get_account():
    account_list = []
    for line in open("account"):
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
    chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    try:
        driver_url = "./chromedriver"
        driver = webdriver.Chrome(driver_url, chrome_options=chrome_options)
        try:
            driver.get("https://weibo.com")
            sleep(10)
            account = driver.find_element_by_id("loginname")
            account.clear()
            account.send_keys(phone)
            pwd = driver.find_element_by_name("password")
            pwd.clear()
            pwd.send_keys(password)
            pwd.send_keys(Keys.RETURN)
            sleep(10)
            cookie_list = driver.get_cookies()
            cookie_obj = dict()
            for item in cookie_list:
                cookie_obj[item['name']] = item['value']
            # print(cookie_obj)
            # cookie = [item["name"] + "=" + item["value"] for item in cookie_list]
            # cookies = '; '.join(item for item in cookie)
            f = open('cookies.txt', 'a')
            f.write(json.dumps(cookie_obj) + '\n')
            f.close()
            driver.quit()
        except Exception as err:
            driver.quit()
            print("error1----->", err)

    except Exception as err:
        print("open brower error", err)


if __name__ == "__main__":
    get_account()
