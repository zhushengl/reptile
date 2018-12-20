# encoding=utf-8

import urllib2
# import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def loadPage(url):
    '''
        作用：根据url发送请求，获取服务器响应文件
        url：需要爬取的url地址
    '''
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)

    # request = urllib.request.Request(url, headers=headers)
    # response = urllib.request.urlopen(request)
    return response.read()

