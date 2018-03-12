# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonsimsItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    name = scrapy.Field()
    star = scrapy.Field()
    price = scrapy.Field()
    imgsrc = scrapy.Field()
    reviews = scrapy.Field()
    level = scrapy.Field()
    
class AmazonsimsList(scrapy.Item):
    code = scrapy.Field()
    sims = scrapy.Field()
