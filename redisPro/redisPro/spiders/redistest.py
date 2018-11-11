# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from redisPro.items import RedisproItem


class RedistestSpider(RedisCrawlSpider):
    name = 'redistest'
    # allowed_domains = ['https://58.com']
    # start_urls = ['https://bj.58.com/']
    redis_key = "58spider"

    link = LinkExtractor(allow=r'https://bj.58.com/chuzu/pn\d+/')
    rules = (
        Rule(link, callback='parse_item', follow=True),
    )

    def pasrseBySecondPage(self, response):
        # print(response.text)
        item = response.meta["item"]
        strongbox = response.xpath(
            "/html/body/div[4]/div[2]/div[2]/div[1]/div[1]/ul/li[3]/span[2]/text()").extract_first().strip()
        phone = response.xpath("/html/body/div[4]/div[2]/div[2]/div[2]/div[1]/span/text()").extract_first().strip()
        pay_type = response.xpath(
            "/html/body/div[4]/div[2]/div[2]/div[1]/div[1]/div/span[2]/text()").extract_first().strip()

        item["strongbox"] = strongbox
        item['phone'] = phone
        item["pay_type"] = pay_type
        yield item

    def parse_item(self, response):
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        # print(response.text)
        # item = response.xpath('//a[@tongji_tag="pc_home_fc_1_1"]/text()').extract_first()
        items = response.xpath('//div[@class="listBox"]/ul/li')
        # print(items)
        for item in items:
            # print(item)
            title = item.xpath('.//div[@class="des"]/h2/a/text()').extract_first().strip()
            link = item.xpath('.//div[@class="des"]/h2/a/@href').extract_first()
            link = "https:%s" % link
            size = item.xpath('.//div[@class="des"]/p[@class="room strongbox"]/text()').extract_first().strip()
            print(title, link, size)
            item_meta = RedisproItem()
            item_meta["title"] = title
            item_meta["link"] = link
            item_meta["size"] = size
            yield scrapy.Request(url=link, callback=self.pasrseBySecondPage, meta={"item": item_meta})

