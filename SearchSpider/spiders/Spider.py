# -*- coding: utf-8 -*-
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from SearchSpider.items import SearchspiderItem
from scrapy.selector import Selector


class Spider(CrawlSpider):

    name = "SearchSpider"
    allowed_domains = ["news.sina.com.cn"]
    start_urls = ['http://news.sina.com.cn']
    rules = [
        Rule(LinkExtractor(allow=('[0-9]\.shtml$', )), callback='parse_item'),
        Rule(LinkExtractor(allow=('/$', )), follow=True),
    ]

    def parse_item(self, response):

        item = SearchspiderItem()
        article = ''
        selector = Selector(response)

        item['link'] = response.url
        item['title'] = re.split(r'|', selector.xpath("/html/head/title/text()").extract()[0])[0]
        for text in selector.xpath("id('artibody')//p/text()").extract():
            article += text.replace('"', '').replace(' ','').strip()
        item['article'] = article

        return item