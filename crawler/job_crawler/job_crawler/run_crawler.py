import scrapy
from scrapy.crawler import CrawlerProcess

from spiders.liepin_spider import LiepinSpider


process = CrawlerProcess()

process.crawl(LiepinSpider)
