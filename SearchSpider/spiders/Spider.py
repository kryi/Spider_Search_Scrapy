# -*- coding: utf-8 -*-
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from SearchSpider.items import SearchspiderItem
from scrapy.selector import Selector
from scrapy import log


class Spider(CrawlSpider):

    name = "SearchSpider"
    allowed_domains = ["news.sina.com.cn", "news.qq.com", "news.ifeng.com",
                       "sports.sina.com.cn", "sports.qq.com", "sports.ifeng.com"
                       ]
    sina_url_list = ['news.sina.com.cn', 'sports.sina.com.cn']
    ifeng_url_list = ['news.ifeng.com', 'sports.ifeng.com']
    qq_url_list = ['news.qq.com', 'sports.qq.com']

    deny_list = ['http://news.sina.com.cn/z/eztxjwdcx/', 'http://news.sina.com.cn/z/jzecore/',
                 'http://news.sina.com.cn/z/dhbrjsj/']
    deny_url = ['eztxjwdcx/$', 'jzecore/$', 'dhbrjsj/$']

    start_urls = ['http://news.sina.com.cn',
                  'http://news.qq.com',
                  'http://news.ifeng.com']
    rules = [
        Rule(LinkExtractor(allow=('[0-9]\.shtml$'), allow_domains=sina_url_list), callback='parse_item'),
        Rule(LinkExtractor(allow=('[0-9]\.htm$'), allow_domains=qq_url_list, deny=deny_url), callback='parse_qq'),
        Rule(LinkExtractor(allow=('[0-9]\.shtml$'), allow_domains=ifeng_url_list), callback='parse_ifeng'),
        Rule(LinkExtractor(allow=('/$', )), follow=True),
    ]


    def parse_ifeng(self, response):

        item = SearchspiderItem()
        item['link'] = response.url
        selector = Selector(response)
        article = ''
        count = 0
        time_class = ['ss01']
        item['time'] = []

        try:
            item['title'] = re.split(r'|', re.split(r'_', selector.
                                                    xpath("/html/head/title/text()").extract()[0])[0])[0]
        except:
            log.msg(item['title'], log.ERROR)
            return
        try:
            for text in selector.xpath("id('artical_real')//p/text()").extract():
                #log.msg(text, log.ERROR)
                article += text.replace('"', '').replace(' ', '') \
                    .replace('\\', '').strip().encode(encoding='utf-8').strip().replace(' ', '')
            item['article'] = article
        except:
            log.msg(item['article'], log.ERROR)
            return
        if item['article'] == '':
            return
        try:
            while(item['time'] == []):
                item['time'] = selector.xpath("//span[@class='" + time_class[count] + "']/text()").extract()
                count = count+1

            item['time'] = item['time'][0].replace(
                '年'.decode(encoding='utf-8'), '-').replace(
                '月'.decode(encoding='utf-8'), '-').replace(
                '日'.decode(encoding='utf-8'), '').encode(encoding="utf-8").strip()
        except:
            log.msg(item['time'], log.ERROR)
            log.msg(item['link'], log.ERROR)
            return

        return item


    def parse_qq(self, response):

        item = SearchspiderItem()
        item['link'] = response.url
        selector = Selector(response)
        time_class = ['article-time', 'a_time', 'pubTime']
        item['time'] = []
        article = ''
        count = 0

        try:
            item['title'] = re.split(r'_', selector.xpath("/html/head/title/text()").extract()[0])[0]
        except:
            log.msg(item['title'], log.ERROR)
            return
        try:
            for text in selector.xpath("id('Cnt-Main-Article-QQ')//p/text()").extract():
                article += text.replace('"', '').replace(' ', '') \
                    .replace('\\', '').strip().encode(encoding='utf-8').strip().replace(' ','')
            item['article'] = article
        except:
            log.msg(item['article'], log.ERROR)
            return
        try:
            while(item['time'] == []):
                #log.msg("//span[@class='" + time_class[count] + "']/text()", log.ERROR)
                item['time'] = selector.xpath("//span[@class='" + time_class[count] + "']/text()").extract()
                count = count+1

            item['time'] = item['time'][0]
        except:
            log.msg(item['time'], log.ERROR)
            log.msg(item['link'], log.ERROR)
            return
        return item


    def parse_item(self, response):

        item = SearchspiderItem()
        article = ''
        selector = Selector(response)
        time_id = ['navtimeSource','pub_date']
        time_class = ['time-source', 'time']
        count = 0
        item['time'] = []

        item['link'] = response.url
        try:
            item['title'] = re.split(r'|', selector.xpath("/html/head/title/text()").extract()[0])[0]
        except:
            log.msg(item['title'], log.ERROR)
            return
        try:
            for text in selector.xpath("id('artibody')//p/text()").extract():
                article += text.replace('"', '').replace(' ', '') \
                    .replace('\\', '').strip().encode(encoding='utf-8').strip().replace(' ','')
            item['article'] = article
        except:
            log.msg(item['article'], log.ERROR)
            return
        #tmp = selector.xpath("id('navtimeSource')/text()").extract()[0]
        #log.msg(tmp,level=log.ERROR)
        try:
            while(item['time'] == []):
                #log.msg("id('" + time_id[count] + "')/text()", log.ERROR)
                item['time'] = selector.xpath("id('" + time_id[count] + "')/text()").extract()
                count = count+1

            if(item['time'] == []):
                count = 0

            # while(item['time'] == []):
            #     item['time'] = selector.xpath("//span[@class='" + time_class[count] + "']/text()").extract()
            #     count = count+1
            #     if(item['time']):
            #         log.msg(item['time'], log.ERROR)

            item['time'] = item['time'][0].replace(
                '年'.decode(encoding='utf-8'), '-').replace(
                '月'.decode(encoding='utf-8'), '-').replace(
                '日'.decode(encoding='utf-8'), ' ').encode(encoding="utf-8").strip()
        except:
            log.msg(item['time'], log.ERROR)
            log.msg(item['link'], log.ERROR)
            return

        #item['heat'] = selector.xpath("id('commentCount1')/text()").extract()[0]
        #log.msg(item['heat'],level=log.ERROR)

        return item