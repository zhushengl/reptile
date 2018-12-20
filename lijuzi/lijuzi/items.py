# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    # 公司id (url数字部分)
    info_id = scrapy.Field()
    # 公司简称
    company_name = scrapy.Field()
    # 公司获投情况
    investment = scrapy.Field()
    # 公司口号
    slogan = scrapy.Field()
    # 投资信息
    investment_info = scrapy.Field()
    # 公司主页
    home_page = scrapy.Field()
    # 公司标签
    tags = scrapy.Field()
    # 公司简介
    company_intro = scrapy.Field()
    # 公司全称
    company_full_name = scrapy.Field()
    # 成立时间
    found_time = scrapy.Field()
    # 公司规模
    company_size = scrapy.Field()
    # 运营状态
    company_status = scrapy.Field()
    # 团队信息列表：包含成员姓名、成员职称、成员介绍
    tm_info = scrapy.Field()

