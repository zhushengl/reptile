# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals
from lijuzi.settings import USER_AGENTS
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.cookies import CookiesMiddleware


class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        self.user_agent = random.choice(USER_AGENTS)
        if self.user_agent:
            request.headers.setdefault('User-Agent', self.user_agent)


class RotateProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://112.115.57.20:3128'


class CookiesMiddleware(object):
    def __init__(self):
        self.cookies = {
            'acw_tc': '76b20f4815378637296801047e5113a4a7b14c2c1b9e490eb93a8808cd0b94',
            '_ga': 'GA1.2.213186077.1537777330',
            'gr_user_id': '2eb2f838-5d24-44c6-a805-7a3186e093b7',
            'MEIQIA_EXTRA_TRACK_ID': '1Ah0t9MVaQndDwEveFRFWeipkw9',
            'identity': '17766344537%40test.com',
            'unique_token': '569904',
            '_gid': 'GA1.2.490846254.1538192708',
            'Hm_lvt_1c587ad486cdb6b962e94fc2002edf89': '1537777331,1538192709',
            'MEIQIA_VISIT_ID': '1ArlhnoWikl74IK4UPzKlMc55Oj',
            'gr_session_id_eee5a46c52000d401f969f4535bdaa78': 'dd53ac47-8a9d-47a6-9268-bc8bcedd678e',
            'gr_session_id_eee5a46c52000d401f969f4535bdaa78_dd53ac47-8a9d-47a6-9268-bc8bcedd678e': 'true',
            'session': 'efcaef7ba3102da36e078cc61491d65bd5da1f43',
            '_gat': '1',
            'remember_code': '9D95Mm8RQd',
            'Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89': '1538195685'
        }

    def process_request(self, request, spider):
        request.cookies = self.cookies


class LijuziSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LijuziDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
