# -*- coding: utf-8 -*-
import scrapy
import os
import requests
import time
from hungrySpider.items import HungryspiderItem
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from lxml import etree
import json
import re
# 用来创建excel文档并写入数据
from openpyxl import Workbook

import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')


class HungrySpider(RedisSpider):
    name = 'hungry'
    # allowed_domains = ['www.ele.me']
    # start_urls = ['http://www.ele.me/home/']
    redis_key = 'hungrySpider:start_urls'
    wb = Workbook()  # class实例化
    ws = wb.active  # 激活工作表
    ws.title = "New Shit1"

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(HungrySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument("--proxy-server=http://112.115.57.20:3128")
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        # 获得主页
        driver.get(response.url)
        time.sleep(3)
        # driver.save_screenshot("1.png")
        driver.find_element_by_xpath('//a[@class="mapcity-current ng-binding"]').click()
        # 获得城市信息
        time.sleep(2)
        driver.find_element_by_name("name").send_keys(u"无锡")
        time.sleep(.5)
        driver.find_element_by_xpath('//ul[@class="mapcity-suggestlist ng-scope"]/li[1]').click()
        time.sleep(.5)
        # 写入收货地址
        driver.find_element_by_xpath('//input[@class="ng-pristine ng-valid"]').send_keys(u"国家软件园")
        time.sleep(.5)
        driver.find_element_by_xpath('//button[@class="btn-stress"]').click()
        time.sleep(.5)
        driver.find_element_by_xpath('//ul[@class="ng-scope"]/li[1]').click()
        time.sleep(3)

        '''
                https://www.ele.me/place/wtte5hkvzhmd?latitude=31.4892&longitude=120.373042

                https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=
                        wtte5hkvzhmd&latitude=31.4892&limit=24&longitude=120.373042&offset=0&terminal=web 
        '''
        # 进入饿了么商家页面
        url_1 = driver.current_url.split('/')[-1]
        byteField_1 = url_1.split('?')[0]
        byteField_2 = re.findall(r'(\w.+)&', url_1.split('=')[-2])[0]
        byteField_3 = url_1.split('=')[-1]

        # 拼接出 抓包工具 抓到的 url
        for offset in range(0, 1201, 24):
            url_2 = 'https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=' + byteField_1 + '&latitude=' + byteField_2 + '&limit=24&longitude=' + byteField_3 + '&offset={}&terminal=web'.format(
                offset)
            yield scrapy.Request(url_2, callback=self.find_all_id)

    def find_all_id(self, response):
        item = HungryspiderItem()
        json_obj = json.loads(response.body)
        for each in json_obj:
            item['address'] = each['address']  # 地址
            item['shopName'] = each['name']  # 店铺
            item['id'] = each['id']
            link = 'https://www.ele.me/restapi/shopping/v2/menu?restaurant_id=' + str(item['id'])
            yield scrapy.Request(link, meta={'meta_1': item}, callback=self.hParse)

    def hParse(self, response):
        json_objs = json.loads(response.body)
        # 获取Request请求发送的meta_1参数
        item = response.meta['meta_1']
        for json_obj in json_objs:
            dict1 = {}
            item['classification'] = json_obj['name']  # 分类
            for food in json_obj['foods']:
                foodList = []
                dict1['foodName'] = food['name']
                dict1['Evaluation'] = re.findall('\d+', food['tips'])[0]  # 评价
                dict1['sale'] = re.findall('\d+', food['tips'])[1]  # 销售
                dict1['rating'] = food['rating']  # 评级
                dict1['price'] = food['specfoods'][0]['price']  # 价格
                foodList.append(dict1)
                item['foodInformation'] = foodList

                yield item


