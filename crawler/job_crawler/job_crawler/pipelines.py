# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from job_crawler.storage.storage_driver import get_storage_driver


class JobCrawlerPipeline(object):
    def process_item(self, item, spider):
        self.store_item(item)

    def store_item(self, item):
        driver = get_storage_driver()

        driver.save_json(item)


        