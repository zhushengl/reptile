# -*- coding: utf-8 -*-
import scrapy
from doubanmovieSpider.items import DoubanmoviespiderItem
import requests
from cStringIO import StringIO
from PIL import Image
import chardet
import time

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']
    # headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
    start = 0
    url = 'https://movie.douban.com/top250?start='
    end = '&filter='

    def start_requests(self):
        url = 'https://www.douban.com/accounts/login'
        yield scrapy.Request(url, callback=self.post_login, meta={'cookiejar': 1})

    def post_login(self, response):
        print 'User-Agent:', response.request.headers.getlist('User-Agent')
        print 'Cookie:', response.request.headers.getlist('Cookie')
        print 'Set-Cookie', response.headers.getlist('Set-Cookie')
        print '登录前表单填充'.decode('utf-8')
        captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract_first()
        captcha_image_url = response.xpath('//img[@id="captcha_image"]/@src').extract_first()
        if captcha_image_url is None:
            print '登录时无验证码'.decode('utf-8')
            formdata = {
                "source": "index_nav",
                "form_email": "2231636899@qq.com",
                # 请填写你的密码
                "form_password": "2231636899@qq.comzsl",
            }
        else:
            print "登录时有验证码".decode('utf-8')
            print captcha_image_url
            rep = requests.get(captcha_image_url, verify=False).content
            image_buff = StringIO(rep)
            img = Image.open(image_buff)
            img.show()
            captcha_solution = raw_input('根据打开的图片输入验证码：'.decode('utf-8'))
            formdata = {
                'source': 'index_nav',
                'form_email': '2231636899@qq.com',
                'form_password': '2231636899@qq.comzsl',
                'captcha-solution': captcha_solution,
                'captcha-id': captcha_id}
        # print response.meta['cookiejar']
        yield scrapy.FormRequest.from_response(response, formdata=formdata, callback=self.after_login)

    def after_login(self, response):
        # yield scrapy.Request("https://www.douban.com/people/184468667/", callback=self.parse_page)  # 主页
        # 访问 （豆瓣电影 Top 250）
        print self.url + str(self.start) + self.end
        yield scrapy.Request(self.url + str(self.start) + self.end, callback=self.post_movie)

    def post_movie(self, response):
        if response.status != 200:
            print '访问出错'
        else:
            print '访问成功'
            movies = response.xpath("//div[@class='info']")
            item = DoubanmoviespiderItem()
            for each in movies:
                title = each.xpath('div[@class="hd"]/a/span[@class="title"]/text()').extract()
                content = each.xpath('div[@class="bd"]/p/text()').extract()
                score = each.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
                info = each.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()

                item['title'] = title[0]
                # 以;作为分隔，将content列表里所有元素合并成一个新的字符串
                item['content'] = ';'.join(content)
                item['score'] = score[0]
                item['info'] = info[0]
                # 提交item
                print title[0]
                yield item

            if self.start <= 100:
                self.start += 25
            print self.url + str(self.start) + self.end
            yield scrapy.Request(self.url + str(self.start) + self.end, callback=self.post_movie)




