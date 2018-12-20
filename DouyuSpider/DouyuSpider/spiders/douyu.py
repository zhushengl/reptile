# -*- coding: utf-8 -*-
import scrapy
import json
from DouyuSpider.items import DouyuspiderItem
import re


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['capi.douyucdn.cn']
    offset = 0
    url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    start_urls = [url + str(offset)]

    def parse(self, response):
        room_data = json.loads(response.body)['data']
        for each in room_data:
            item = DouyuspiderItem()
            name = each['nickname']
            image_url = each['vertical_src']
            item['name'] = name
            item['image_url'] = image_url
            yield item

        self.offset += 20
        next_url = re.sub('offset=\d+', 'offset='+str(self.offset), response.url)
        print next_url
        yield scrapy.Request(next_url, callback=self.parse)


