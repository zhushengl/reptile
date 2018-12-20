# -*- coding: utf-8 -*-
import scrapy
from doubanmovieSpider.items import DoubanmoviespiderItem

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class DoubanbooksSpider(scrapy.Spider):
    name = 'doubanbooks'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']

    start = 0
    url = 'https://book.douban.com/top250?start='
    end = '&filter='

    def start_requests(self):
        # 访问 （豆瓣图书 Top 250）
        print self.url + str(self.start) + self.end
        yield scrapy.Request(self.url + str(self.start) + self.end, callback=self.post_book)

    def post_book(self, response):
        if response.status == 200:
            print '访问成功'
            # print response.body
            books = response.xpath("//div[@class='article']//table")
            item1 = DoubanmoviespiderItem()
            for each in books:
                print each
                title = each.xpath("//td[2]/div/a/text()").extract()
                print title[0]
                content = each.xpath("//p[1]/text()").extract()
                score = each.xpath("//div/span[2]/text()").extract()
                info = each.xpath("//p[2]/span/text()").extract()

                item1['title'] = title[0]
                # 以;作为分隔，将content列表里所有元素合并成一个新的字符串
                item1['content'] = ';'.join(content)
                item1['score'] = score[0]
                item1['info'] = info[0].strip()
                # 提交item
                print item1
                yield item1

            if self.start <= 100:
                self.start += 25
            print self.url + str(self.start) + self.end
            yield scrapy.Request(self.url + str(self.start) + self.end, callback=self.post_book)
        else:
            print '访问失败'

    def parse(self, response):
        pass
