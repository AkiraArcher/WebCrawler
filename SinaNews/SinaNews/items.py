# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class SinaNews(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    headline = Field()
    summary = Field()
    link = Field()
    date = Field()
    source = Field()
    comment = Field()
    comment_pages = Field()
    news_id = Field()
    old = Field()
