# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import Spider
from scrapy.selector import Selector

from SinaNews.items import SinaNews

import time
import json
import re

class SinanewsSpider(scrapy.Spider):
    name = "sinaNews"
    allowed_domains = ["news.sina.com.cn"]
    page = 1

    url1 = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page='
    url2 = '&callback=newsloadercallback'

    url3 = 'http://comment5.news.sina.com.cn/page/info?format=js&channel=gn&newsid=comos-'
    url4 = '&group=0&compress=1&ie=gbk&oe=gbk&page='
    url5 = '&page_size=20'

    url6 = 'http://comment5.news.sina.com.cn/page/info?format=js&channel=gn&newsid=1-1-'
    url7 = '&group=0&compress=1&ie=gbk&oe=gbk&page='
    url8 = '&page_size=100'
    start_urls = [
        'http://news.sina.com.cn/china/'
        
    ]


    def parse(self, response):
        while self.page < 2:

            next_page = self.url1 + str(self.page) + self.url2
            yield scrapy.Request(next_page, callback=self.parse_news)
            self.page += 1

    def parse_news(self, response):
        ss = response.body.replace("newsloadercallback(","")
        ss = ss[:-2]
        
        datas = json.loads(ss)
        print "\n"
        print "-----------------The roll_page is: " + response.request.url
        print "\n"
        for data in datas['result']['data']:
            item1 = SinaNews()
            item1['headline'] = data['title']
            item1['summary'] = data['ext5']
            item1['date'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(data['createtime'])))
            item1['link'] = data['url']
            item1['source'] = ""
            item1['old'] = False
            item1['comment'] = []
            STR = str(re.findall(r'doc-i(.+?).shtml', data['url']))
            item1['news_id'] =  STR[3:len(STR)-2]
            print "\n"
            print "-----------------The news_page is: " + item1['link']
            print "\n"
            item1['comment_pages'] = 1

            if item1['news_id'] == "":
                STR = str(re.findall(r'cn/c/.*/\d{4}(.*?).shtml', data['url']))
                item1['news_id'] =  STR[3:len(STR)-2]
                item1['old'] = True
                comment_url = self.url6 + item1['news_id'] + self.url7 + str(1) + self.url8
            else :
                comment_url = self.url3 + item1['news_id'] + self.url4 + str(1) + self.url5

            if item1['news_id'] != "":
                print "\n"
                print "------------The 1 comment_page is :  " +  comment_url
                print "\n"
                yield scrapy.Request(comment_url, meta={'item': item1}, callback=self.parse_comment)
            else :
                continue
            


    def parse_comment(self, response):
        item1 = response.meta['item']  
        
        cmt = response.body[response.body.find('=')+1:]
        cmts = json.loads(cmt)
        print "--------------------------------"
        print str(item1['news_id']) + ":" + str(item1['comment_pages'])
        if  cmts['result'].has_key('cmntlist') :
            print len(cmts['result']['cmntlist'])
            print "--------------------------------"
            for data in cmts['result']['cmntlist'] :
                arr = {}
                arr['area'] = data['area']
                arr['content'] = data['content']
                arr['ip'] = data['ip']
                arr['length'] = data['length']
                arr['level'] = data['level']
                arr['mid'] = data['mid']
                arr['newsid'] = data['newsid']
                arr['nick'] = data['nick']
                arr['time'] = data['time']
                arr['uid'] = data['uid']
                arr['usertype'] = data['usertype']
                arr['vote'] = data['vote']
                #print item1.keys()
                item1['comment'].append(arr)

            item1['comment_pages'] += 1
            if item1['old'] == True :
                comment_url = self.url6 + item1['news_id'] + self.url7 + str(item1['comment_pages']) + self.url8
            comment_url = self.url3 + str(item1['news_id']) + self.url4 + str(item1['comment_pages']) + self.url5

            print "\n"
            print "------------The " + str(item1['comment_pages']) + " comment_page is :  " +  comment_url
            print "\n"
            yield scrapy.Request(comment_url, meta={'item': item1}, callback=self.parse_comment)
        else:
            yield scrapy.Request(item1['link'], meta={'item': item1}, callback=self.parse_source)


    def parse_source(self, response):
        item1 = response.meta['item']
        sel = Selector(response)    
        item1['source'] = "".join(sel.xpath('//*[@id="navtimeSource"]/span/span/a/text()').extract())
        if item1['source'] == "":                
            item1['source'] = "".join(sel.xpath('//*[@id="media_name"]/span/a[1]/text()').extract())
        if item1['source'] == "":
            item1['source'] = "".join(sel.xpath('//*[@id="media_name"]/a[1]/text()').extract())
        if item1['source'] == "":
            item1['source'] = "".join(sel.xpath('//*[@id="media_name"]/text()').extract())
                                                
        print "\n"
        print "-------------------" + str(item1['news_id']) + item1['source'] + " is over"
        print "\n"
        return item1




