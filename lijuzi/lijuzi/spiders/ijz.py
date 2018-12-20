# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from lxml import etree
from bs4 import BeautifulSoup
from lijuzi.items import CompanyItem
from scrapy_redis.spiders import RedisSpider


class IjzSpider(RedisSpider):
    name = 'ijz'
    allowed_domains = ['itjuzi.com']
    redis_key = 'ltjuzispider:starturls'

    def start_requests(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--proxy-server=http://112.115.57.20:3128")
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        driver.get('https://www.itjuzi.com/user/login')
        time.sleep(3)
        driver.find_element_by_id('create_account_email').send_keys('17766344537')
        driver.find_element_by_id('create_account_password').send_keys('ye333222')
        driver.find_element_by_id('login_btn').click()
        time.sleep(3)
        driver.get('http://radar.itjuzi.com/company')
        time.sleep(3)

        html = driver.page_source
        selector = etree.HTML(html)
        company_list = selector.xpath('//li[contains(@data-id, "3342")]')
        for company in company_list:
            if company.xpath('./a/@href'):
                link = company.xpath('./a/@href')[0]
            yield scrapy.Request(link, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')

        # 公司头部，基本介绍
        cpy1 = soup.find('div', class_='infoheadrow-v2')
        if cpy1:
            # 公司简称
            company_name = cpy1.find(class_='title').h1['data-name']
            # 获投情况
            investment = cpy1.find(class_='title').h1.span.get_text()
            # 口号
            slogan = cpy1.find(class_='info-line').h2.get_text()
            # 投资详情
            investment_info = cpy1.find_all(class_='info-line')[1].span.get_text()
            # 主页地址
            home_page = cpy1.find(class_='link-line').find_all('a')[-1]['href']
            # 标签
            tags = ','.join(cpy1.find(class_='tagset').get_text().split())

        # 公司主体，详细信息
        cpy2 = soup.find('div', class_='block-inc-info')
        if cpy2:
            # 公司简介
            company_intro = cpy2.find_all(class_='block')[1].find_all('div')[-1].get_text().strip()
            # 公司全称
            company_full_name = cpy2.find(class_='des-more').h2.get_text()
            # 成立时间
            found_time = cpy2.find(class_='des-more').find_all('h3')[0].get_text()[4:]
            # 公司规模
            company_size = cpy2.find(class_='des-more').find_all('h3')[1].get_text()[5:]
            # 运营状态
            company_status = cpy2.find(class_='des-more').find_all('span')[-1].get_text()

        # 团队信息
        cpy3 = soup.find('ul', class_='list-unstyled team-list limited-itemnum')
        tm_list = []
        if cpy3:
            for li in cpy3.find_all('li'):
                tm_dict = {}
                tm_dict['tm_m_name'] = li.find_all('div')[0].a.get_text()
                tm_dict['tm_m_title'] = li.find_all('div')[1].get_text()
                tm_dict['tm_m_intro'] = li.find_all('div')[2].div.get_text().strip()
                tm_list.append(tm_dict)

        item = CompanyItem()
        item['info_id'] = response.url.split('/')[-1]
        item['company_name'] = company_name
        item['investment'] = investment
        item['slogan'] = slogan
        item['investment_info'] = investment_info
        item['home_page'] = home_page
        item['tags'] = tags
        item['company_intro'] = company_intro
        item['company_full_name'] = company_full_name
        item['found_time'] = found_time
        item['company_size'] = company_size
        item['company_status'] = company_status
        item['tm_info'] = tm_list

        return item
