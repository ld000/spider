# -*- coding: UTF-8 -*-
from amazonsims.items import *
import scrapy
import json

class amazonsimsSpider(scrapy.Spider):
    name = "amazonsims"
    allowed_domains = ["amazon.com", "www.amazon.com", "amazon.cn", "www.amazon.cn"]
    download_delay = 2
    level = 1
    # start_urls = [
    #       'https://www.amazon.cn/gp/product/B06XSWSQLN/ref=pd_sim_147_1?ie=UTF8&psc=1&refRID=7RQSCK3S97Y77VH1BHDS',
    # ]
    # rules = [
    #     Rule(LinkExtractor(allow=("/product/.*")), callback='parse_item'), 
    # ]
# restrict_xpaths=('//div[@id="purchase-sims-feature"]',)

    def start_requests(self):
        urls = [
            'https://www.amazon.cn/gp/product/B06XSWSQLN/ref=pd_sim_147_1?ie=UTF8&psc=1&refRID=7RQSCK3S97Y77VH1BHDS',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'level': self.level})

    def parse(self, response):
      # stuff = AmazonsimsList()
      # stuff['code'] = 'B06XSWSQLN'
      # stuff['sims'] = []

      urls = []

      # print response.body
      # print response.css('#purchase-sims-feature').extract()
      # print '---------'
      # print response.css('#purchase-sims-feature > div::attr(data-a-carousel-options)').extract()


      print '-------'
      print response.url
      if '请输入您在这个图片中看到的字符' in response.body:
        print '进入输入验证码页面了---------------------'
        return


      # -----------------------
      # build url
      # -----------------------

      # print response.body
      # print response.css('#purchase-sims-feature')
      # print len(response.css('#purchase-sims-feature'))
      if len(response.css('#purchase-sims-feature')) == 0:
          featureName = response.css('#session-sims-feature > div::attr(data-p13n-feature-name)')[0].extract()
          ajaxStr = response.css('#session-sims-feature > div::attr(data-a-carousel-options)')[0].extract()
      else:
          featureName = response.css('#purchase-sims-feature > div::attr(data-p13n-feature-name)')[0].extract()
          ajaxStr = response.css('#purchase-sims-feature > div::attr(data-a-carousel-options)')[0].extract()

      # print ajaxStr
      ajaxJson = json.loads(ajaxStr)

      relatedRequestId = ajaxJson['ajax']['params']['relatedRequestID']
      idList = ajaxJson['ajax']['id_list']
      i = 1
      for id in idList:
        s = '/gp/product/' + id + '/ref=' + featureName + '_' + str(i) + '?ie=UTF8&psc=1&refRID=' + relatedRequestId
        urls.append(s)
        i = i + 1
      
      # -----------------------
      # build item object
      # -----------------------

      item = AmazonsimsItem()
      item['name'] = response.css('#productTitle ::text')[0].extract().strip()
      item['url'] = response.url
      item['imgsrc'] = response.css('#imgTagWrapperId > img ::attr(data-a-dynamic-image)').extract()
      item['price'] = response.css('#priceblock_ourprice::text').extract()
      item['star'] = response.css('.a-icon.a-icon-star > span::text')[0].extract()
      item['reviews'] = response.css('#acrCustomerReviewText::text')[0].extract()
      item['level'] = response.meta['level']

      yield item

      # list = response.css('.a-carousel-card')
      # for one in list:
      #   item = AmazonsimsItem()
      #   item['url'] = one.css('.a-link-normal ::attr(href)')[0].extract()
      #   item['imgsrc'] = one.css('img ::attr(src)')[0].extract()
      #   item['price'] = one.css('.p13n-sc-price ::text').extract()
      #   item['name'] = one.css('img ::attr(alt)')[0].extract()
      #   item['star'] = one.css('.a-icon-row').css('.a-spacing-none').css('.a-link-normal ::attr(title)').extract()
      #   item['reviews'] = one.css('a').css('.a-size-small::text').extract()
      #   item['level'] = response.meta['level']

      #   yield item
        # stuff['sims'].append(item)

      # yield stuff

      # -----------------------
      # yield next level url
      # -----------------------

      response.meta['level'] = response.meta['level'] + 1
      if int(float(response.meta['level'])) < 5:
        for urlx in urls:
          if (urlx[0] == 'h'):
              url = urlx
          else:
              url = 'https://www.amazon.cn' + urlx
          # print '---------'
          # print url
          yield scrapy.Request(url=url, callback=self.parse, meta=response.meta)


