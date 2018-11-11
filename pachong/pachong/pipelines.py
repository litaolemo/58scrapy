# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PachongPipeline(object):

    def __init__(self):
        self.f = None

    def open_spider(self,spider):
        self.f = open("./58租房.txt","w",encoding="utf-8")

    def process_item(self, item, spider):
        self.f.write(item['title'] + ":" + item['link'] + item['size'] + item['strongbox']+item['phone']+item['pay_type']+"\n")
        self.f.flush()
        return item

    def close_spider(self,spider):
        self.f.close()