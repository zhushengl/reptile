# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class HungryspiderPipeline(object):
    def process_item(self, item, spider):
        # 写入hungry.json
        # data = dict(item)
        # content = json.dumps(data, ensure_ascii=False).encode('utf-8')
        # with open('hungry.json', 'a') as f:
        #     f.write(content)
        return item
