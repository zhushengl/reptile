# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem
import os


class DouyuspiderPipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        url = item['image_url']
        yield scrapy.Request(url)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        #print image_path[0]
        if not image_path:
            raise DropItem('Image_path is null')
        os.rename(self.IMAGES_STORE + '\\' + image_path[0], self.IMAGES_STORE + '\\' + item['name'] + '.jpg')
        item['image_path'] = self.IMAGES_STORE + '\\' + item['name']

        return item


