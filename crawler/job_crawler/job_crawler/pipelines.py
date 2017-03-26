# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from job_crawler.storage.storage_driver import get_storage_driver
from job_crawler.items import JobItem
from job_crawler.storage.storage_driver import get_storage_driver


class JobCrawlerPipeline(object):
    def process_item(self, item, spider):
        self.storage_driver.write(dict(item))

    def close_spider(self, spider):
        self.storage_driver.close()

    def open_spider(self, spider):
        self.storage_driver = get_storage_driver(keys=JobItem.fields.keys())
        self.storage_driver.init()
