# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
# import sys,io
# sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

class TongchengSpider(scrapy.Spider):
    name = 'tongcheng'
    allowed_domains = ['58.com']
    start_urls = ['https://bj.58.com/chuzu/']

    def parse(self, response):
        #print(response.text)
        #item = response.xpath('//a[@tongji_tag="pc_home_fc_1_1"]/text()').extract_first()
        items = response.xpath('//div[@class="listBox"]/ul/li')
        #print(items)
        for item in items:
            #print(item)
            title = item.xpath('.//div[@class="des"]/h2/a/text()').extract_first()
            link = item.xpath('.//div[@class="des"]/h2/a/@href').extract_first()
            size = item.xpath('.//div[@class="des"]/p[@class="room strongbox"]/text()').extract_first().strip()
            print(title,link,size)



