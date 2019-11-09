# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class SearchItem(scrapy.Item):
    # 用户昵称
    user_name = scrapy.Field(output_processor=TakeFirst())
    # 用户ID
    user_id = scrapy.Field(output_processor=TakeFirst())
    # 认证信息
    user_verified_reason = scrapy.Field(output_processor=TakeFirst())
    # 用户描述
    user_description = scrapy.Field(output_processor=TakeFirst())
    # 用户粉丝数
    user_followers_count = scrapy.Field(output_processor=TakeFirst())
    # 用户发微博数
    user_statuses_count = scrapy.Field(output_processor=TakeFirst())
    # 转发数
    reposts_count = scrapy.Field(output_processor=TakeFirst())
    # 评论数
    comments_count = scrapy.Field(output_processor=TakeFirst())
    # 点赞数
    attitudes_count = scrapy.Field(output_processor=TakeFirst())
    # 微博内容
    user_content = scrapy.Field(output_processor=TakeFirst())
    # 发送时间
    created_at = scrapy.Field(output_processor=TakeFirst())
    # 发送来源
    source = scrapy.Field(output_processor=TakeFirst())
    # 微博ID
    mid = scrapy.Field(output_processor=TakeFirst())
    # 查询评论的ID
    idstr = scrapy.Field(output_processor=TakeFirst())
    # 附图
    user_pics = scrapy.Field(output_processor=TakeFirst())


class ReplyItem(scrapy.Item):
    # 用户回复
    user_reply = scrapy.Field(output_processor=TakeFirst())
    # 用户昵称
    user_name = scrapy.Field(output_processor=TakeFirst())
    # 用户ID
    user_id = scrapy.Field(output_processor=TakeFirst())
    # 回复时间
    created_at = scrapy.Field(output_processor=TakeFirst())
    # 微博回复ID
    idstr = scrapy.Field(output_processor=TakeFirst())
    # 此条回复ID
    reply_id = scrapy.Field(output_processor=TakeFirst())
    # 查询时间
    fetchTime = scrapy.Field(output_processor=TakeFirst())
    # 二级回复的父ID 一级回复为空
    root_reply_id = scrapy.Field(output_processor=TakeFirst())
    # 附图
    img_url = scrapy.Field(output_processor=TakeFirst())
    # 认证信息
    user_verified_reason = scrapy.Field(output_processor=TakeFirst())
    # 用户描述
    user_description = scrapy.Field(output_processor=TakeFirst())
    # 用户粉丝数
    user_followers_count = scrapy.Field(output_processor=TakeFirst())
    # 用户发微博数
    user_statuses_count = scrapy.Field(output_processor=TakeFirst())
    # 回复数
    comments_count = scrapy.Field(output_processor=TakeFirst())
    # 点赞数
    attitudes_count = scrapy.Field(output_processor=TakeFirst())
