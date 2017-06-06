# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json

class SinanewsPipeline(object):
    out = file("C:\\Users\\22810\\code\\Python\\WebCrawler Project\\SinaNews\\SinaNews\\SinaNews.json", "w")
    def __init__(self):
        self.ids_seen = set()
        
    def process_item(self, item, spider):
        if item['headline'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item['headline'])
        else:
            print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<" + str(item['news_id']) + "is saved"
            line = json.dumps(dict(item), indent = 2, ensure_ascii=False).encode("utf-8")
            self.out.write(line)
        return item

    def spider_closed(self, spider):
            self.out.close()  