# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaspiderItem(scrapy.Item):
    # 大类的标题
    parent_title = scrapy.Field()
    # 大类的url
    parent_url = scrapy.Field()
    # 小类的标题
    sub_title = scrapy.Field()
    # 小类的url
    sub_url = scrapy.Field()
    # 小类的存储路径
    sub_path = scrapy.Field()
    # 文章的url
    file_url = scrapy.Field()
    # 文章的标题
    file_title = scrapy.Field()
    # 文章的内容
    file_content = scrapy.Field()
    # 获取分布式爬取的当前时间
    crawled = scrapy.Field()
    # 获取分布式爬取的spider名字
    spider = scrapy.Field()
