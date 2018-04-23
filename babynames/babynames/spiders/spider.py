# -*- coding: UTF-8 -*-

import scrapy
from scrapy import Request, FormRequest
from babynames.items import *

class babynamesSpider(scrapy.Spider):
  name = "babynames"
  allowed_domains = ["www.familyeducation.com", "familyeducation.com"]
  download_delay = 1
  start_urls = [
        'https://www.familyeducation.com/baby-names/browse-origin/surname',
  ]

  def start_requests(self):  
    for url in self.start_urls:          
      yield Request(url)

  def parse(self, response):
    countries = response.css('#block-babynamebybrowseoriginblock a::text').extract()

    for country in countries:
      url = self.start_urls[0] + '/' + country
      yield scrapy.Request(url=url, callback=self.countryParse, meta={'country': country, 'page': 0})

  def countryParse(self, response):
    country = response.meta['country']
    page = response.meta['page']

    print '----- country: ' + country + ', page: ' + str(page)

    names = response.css('#block-fentheme-content .baby-names-list a::text').extract()
    for name in names:
      item = BabynamesItem()
      item['name'] = name
      yield item

    #是否有下一页
    nextFlag = response.css('.pager__item.pager__item--last').extract()
    if len(nextFlag):
      nextPage = int(page) + 1

      url = self.start_urls[0] + '/' + country + '?page=' + str(nextPage)
      yield scrapy.Request(url=url, callback=self.countryParse, meta={'country': country, 'page': nextPage})