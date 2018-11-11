# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
# import sys,io
# sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
from ..items import PachongItem

class TongchengSpider(scrapy.Spider):
    name = 'tongcheng'
    #allowed_domains = ['58.com']
    start_urls = ['https://bj.58.com/chuzu/']
    page = 0
    def pasrseBySecondPage(self,response):
        #print(response.text)
        item = response.meta["item"]
        strongbox = response.xpath("/html/body/div[4]/div[2]/div[2]/div[1]/div[1]/ul/li[3]/span[2]/text()").extract_first().strip()
        phone = response.xpath("/html/body/div[4]/div[2]/div[2]/div[2]/div[1]/span/text()").extract_first().strip()
        pay_type = response.xpath("/html/body/div[4]/div[2]/div[2]/div[1]/div[1]/div/span[2]/text()").extract_first().strip()

        item["strongbox"]=strongbox
        item['phone']=phone
        item["pay_type"]=pay_type
        yield item

    def parse(self, response):
        #print(response.text)
        #item = response.xpath('//a[@tongji_tag="pc_home_fc_1_1"]/text()').extract_first()
        items = response.xpath('//div[@class="listBox"]/ul/li')
        #print(items)
        for item in items:
            #print(item)
            title = item.xpath('.//div[@class="des"]/h2/a/text()').extract_first().strip()
            link = item.xpath('.//div[@class="des"]/h2/a/@href').extract_first()
            link = "https:%s" % link
            size = item.xpath('.//div[@class="des"]/p[@class="room strongbox"]/text()').extract_first().strip()
            print(title,link,size)
            item_meta = PachongItem()
            item_meta["title"] = title
            item_meta["link"] = link
            item_meta["size"] = size
            yield scrapy.Request(url=link,callback=self.pasrseBySecondPage,meta={"item":item_meta})

        if self.page <= 2:
            url = format("https://bj.58.com/chuzu/pn%s/" % self.page)
            self.page += 1
            yield scrapy.Request(url=url, callback=self.parse)

