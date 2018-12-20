# encoding=utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
from lxml import etree
from Queue import Queue
import threading
import json
import chardet
import loadHtml

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class douBan(object):
    def __init__(self):
        self.search = {}
        self.books = []
        self.url1 = None
        global driver

    def load(self):
        driver.get("http://www.douban.com")
        time.sleep(3)

        # 生成登陆前快照
        driver.save_screenshot("douban_captcha.png")
        # 取出验证码图片的url地址

        captchaUrl = driver.find_element_by_xpath('//img[@id="captcha_image"]')
        print captchaUrl.get_attribute("src")

        with open('captcha.jpg', 'wb') as f:
            f.write(loadHtml.loadPage(captchaUrl.get_attribute("src")))  # 使用 urllib2
            print "captcha.jpg is ok"

        driver.find_element_by_id("form_email").send_keys('2231636899@qq.com')
        driver.find_element_by_id("form_password").send_keys('2231636899@qq.com')

        captcha = raw_input('输入验证码：')
        driver.find_element_by_id("captcha_field").send_keys(captcha)

        # 模拟点击登录
        # driver.find_element_by_xpath("//input[@class='bn-submit']").click()
        driver.find_element_by_class_name('bn-submit').click()

        # 等待2秒
        time.sleep(2)

        # 生成登陆后快照
        driver.save_screenshot("douban.png")
        html = driver.page_source

        # with open("douban.html", "w") as file:
        #     file.write(driver.page_source)

    def doubanbook(self):
        driver.get("https://book.douban.com/")
        time.sleep(3)
        html = driver.page_source
        # print html

        more_dict = {}
        selector = etree.HTML(html)
        # print etree.tostring(selector)

        title = selector.xpath('//div[@class="section books-express "]/div[@class="hd"]/h2/span[1]/text()')  # 新书速递
        print 'title:', title[0]
        more = selector.xpath('//div[@class="section books-express "]/div[@class="hd"]/h2/span[2]/a/text()')  # 更多»
        print 'more:', more[0]
        url = selector.xpath('//div[@class="section books-express "]/div[@class="hd"]/h2/span[2]/a/@href')[0]

        # {'新书速递':{'更多»':'https://book.douban.com/latest?icn=index-latestbook-all'}}
        self.url1 = 'https://book.douban.com' + url
        more_dict[more[0]] = self.url1
        self.search[title[0]] = more_dict
        print 'self.search:', self.search

        driver.get(self.url1)
        time.sleep(2)
        new_html = driver.page_source

        new_selector = etree.HTML(new_html)
        book1 = new_selector.xpath('//div[@class="article"]//h2//a/@href')
        book2 = new_selector.xpath('//div[@class="aside"]//h2//a/@href')

        self.books.append(book1)  # 虚构类
        self.books.append(book2)  # 非虚构类

        print 'self.books：'
        for i in self.books:
            print i

    def lookfor(self):
        driver.get(self.url1)
        time.sleep(2)
        search_text = raw_input('输入要查找的信息：')
        driver.find_element_by_id("inp-query").clear()
        driver.find_element_by_id("inp-query").send_keys(search_text)
        # driver.find_element_by_id("submit").click()
        driver.find_element_by_xpath('//input[@type="submit"]').send_keys(Keys.RETURN)
        print driver.current_url

        driver.get(driver.current_url)
        html = driver.page_source

        print ("输出搜索的前3页：")
        a = 1
        book_list = []
        while a < 4:
            bookname = driver.find_elements_by_class_name('title-text')
            for i in bookname:
                print i.text
            book_list.append(bookname)

            # 在next位置单击
            ac = driver.find_element_by_xpath('//a[@class="next"]')
            ActionChains(driver).move_to_element(ac).click(ac).perform()
            driver.get(driver.current_url)
            a = a + 1

    def threadParserstart(self):
        global bookUrlQueue
        file = open("douban.json", 'a')
        lock = threading.Lock()

        for i in range(len(self.books)):
            for book in self.books[i]:
                bookUrlQueue.put(book)

            # 创建解析进程
            parserThreadList = []
            thread = ThreadParser(lock, file)
            thread.start()
            time.sleep(1)
            parserThreadList.append(thread)

            for thread in parserThreadList:
                thread.join()

            file.close()
            driver.quit()

    def main(self):
        self.load()
        # -->豆瓣新书-->新书速递
        self.doubanbook()
        yes_no = raw_input("使用搜索（Y/N）")
        if yes_no == 'y' or yes_no == 'Y':
            self.lookfor()
        yes_no = raw_input("爬取新书速递（Y/N）")
        if yes_no == 'y' or yes_no == 'Y':
            self.threadParserstart()


class ThreadParser(threading.Thread):
    def __init__(self, lock, file):
        threading.Thread.__init__(self)
        self.lock = lock
        self.file = file
        global bookUrlQueue
        global driver

    def run(self):
        print "启动线程"
        while not bookUrlQueue.empty():
            try:
                url = bookUrlQueue.get()
                self.parse(url)
            except:
                pass
        print "结束线程"

    def parse(self, url):

        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        new_html = etree.HTML(html)
        print ("#" * 10)

        items = []
        item = {}

        bookName = new_html.xpath('//div[@class="subject clearfix"]//div[@id="mainpic"]//a/@title')[0]
        author = new_html.xpath('//div[@class="subject clearfix"]//span[1]/a/text()')[0]
        imgUrl = new_html.xpath('//div[@class="subject clearfix"]//div[@id="mainpic"]/a/@href')[0]
        comments = new_html.xpath('//div[@class="indent"]//div[@class="intro"]/p/text()')[0]

        item['bookName'] = bookName
        item['author'] = author
        item['imgUrl'] = imgUrl
        item['comments'] = comments

        print item
        items.append(item)
        lines = json.dumps(items, ensure_ascii=False)
        content = lines.encode('utf-8') + "\n"
        print 'content:', content

        self.lock.acquire()
        self.file.write(content)
        self.lock.release()


if __name__ == '__main__':
    driver = webdriver.Chrome()
    bookUrlQueue = Queue()

    start = douBan()
    start.main()
