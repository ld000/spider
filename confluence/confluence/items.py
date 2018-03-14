# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ConfluenceItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    path = scrapy.Field()
    content = scrapy.Field()

class ImgItem(scrapy.Item):
    name = scrapy.Field()
    path = scrapy.Field()
    content = scrapy.Field()
