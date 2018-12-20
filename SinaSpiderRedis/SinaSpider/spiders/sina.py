# -*- coding: utf-8 -*-
import scrapy
import os
from SinaSpider.items import SinaspiderItem
from scrapy_redis.spiders import RedisSpider


class SinaRedisSpider(RedisSpider):
    name = 'sina1'
    redis_key = 'sinaredisspider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(SinaRedisSpider, self).__init__(*args, **kwargs)

    # 解析首页
    def parse(self, response):
        # 获取大类的标题列表
        parent_title_list = response.xpath('//div[@id="tab01"]//h3/a/text()').extract()
        # 获取大类的链接列表
        parent_link_list = response.xpath('//div[@id="tab01"]//h3/a/@href').extract()
        # 遍历大类列表
        for i in range(len(parent_title_list)):
            # 根据大类的标题名新建目录
            parent_path = '.\\Data\\' + parent_title_list[i]
            if not os.path.exists(parent_path):
                os.makedirs(parent_path)
            # 获取每个大类下的小类的标题列表
            sub_title_list = response.xpath('//div[@id="tab01"]/div[{}]//li/a/text()'.format(i + 1)).extract()
            # 获取每个大类下的小类的url列表
            sub_link_list = response.xpath('//div[@id="tab01"]/div[{}]//li/a/@href'.format(i + 1)).extract()
            # 遍历某一个大类下的小类列表
            for j in range(len(sub_title_list)):
                # 根据小类的标题名新建目录
                sub_path = parent_path + '\\' + sub_title_list[j]
                if not os.path.exists(sub_path):
                    os.makedirs(sub_path)
                item = SinaspiderItem()
                item['parent_title'] = parent_title_list[i]
                item['parent_url'] = parent_link_list[i]
                item['sub_title'] = sub_title_list[j]
                item['sub_url'] = sub_link_list[j]
                item['sub_path'] = sub_path
                # 发送每个小类的Request请求，在Request中加入meta，即可将meta传递给response作为参数给回调函数使用
                yield scrapy.Request(item['sub_url'], callback=self.parse_sub, meta={'meta_1': item})

    # 解析每个小类的url，爬取每个小类下的文章标题和链接
    def parse_sub(self, response):
        # 获取Request请求发送的meta_1参数
        item = response.meta['meta_1']
        # 获取新闻的链接
        news_links = response.xpath('//a/@href').re(r'.*\d+\.shtml')
        for i in range(len(news_links)):
            # 根据新闻的链接获取新闻的标题
            file_title = response.xpath('//a[@href="%s"]/text()' % news_links[i]).extract_first()
            item['file_url'] = news_links[i]
            item['file_title'] = file_title
            # 发送每篇新闻的Request请求，在Request中加入meta，向回调函数parse_content传递参数meta1
            yield scrapy.Request(item['file_url'], callback=self.parse_news, meta={'meta_1': item})

    # 解析每个新闻页，获取新闻标题和内容
    def parse_news(self, response):
        # 获取Request请求发送的meta_1参数
        item = response.meta['meta_1']
        content_list = response.xpath('//div[@class="article"]//p/text()|//div[@id="artibody"]//p/text()').extract()
        # 获取新闻的内容
        content = item['file_url'] + '\n' + ''.join(content_list)
        item['file_content'] = content

        yield item
