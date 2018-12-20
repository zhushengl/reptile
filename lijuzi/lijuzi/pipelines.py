# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class LijuziPipeline(object):
    def process_item(self, item, spider):
        data = dict(item)
        content = json.dumps(data, ensure_ascii=False).encode('utf-8')
        with open('company.json', 'a') as f:
            f.write(content)
        return item
