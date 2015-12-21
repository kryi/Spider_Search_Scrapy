# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import io
from scrapy import log


class SearchspiderPipeline(object):

    count = 1

    def process_item(self, item, spider):
        item['id'] = self.count
        path = '/Users/liujingkun/Exp/python/scrapy/SearchSpider/SearchSpider/data/' \
               + str(self.count) + '.json'
        with io.open(path, mode='w', encoding='utf-8') as fp:
            jsondata = json.dumps(dict(item)) + '\n'
            fp.write(jsondata.decode('unicode_escape'))
        self.count = self.count + 1
        return item
