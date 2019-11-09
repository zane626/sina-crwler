from scrapy.cmdline import execute

cmdStr = "scrapy crawl weibo_search -a keyword=鹿晗 -a reply=True".split()
execute(cmdStr)
# from scrapy.cmdline import execute
# import os, sys
#
# print(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#
# execute(['scrapy', 'runspider', 'wechat/spiders/sogou_wechat.py'])
