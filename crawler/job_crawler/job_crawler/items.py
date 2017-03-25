# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()

    require_degree = scrapy.Field()
    work_experience = scrapy.Field()
    required_skills = scrapy.Field()
    required_age = scrapy.Field()

    tags = scrapy.Field()

    job_description = scrapy.Field()

    company_name = scrapy.Field()
    company_description = scrapy.Field()

    position = scrapy.Field()
    pub_date = scrapy.Field()
