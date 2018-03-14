# -*- coding: UTF-8 -*-

import scrapy
from scrapy import Request, FormRequest
from confluence.items import *
import time
import urlparse
import logging

# script = """
# function main(splash)
#   splash:init_cookies(splash.args.cookies)
#   assert(splash:go{
#     splash.args.url,
#     headers=splash.args.headers,
#     http_method=splash.args.http_method,
#     body=splash.args.body,
#     })
#   assert(splash:wait(0.5))

#   local entries = splash:history()
#   local last_response = entries[#entries].response
#   return {
#     url = splash:url(),
#     headers = last_response.headers,
#     http_status = last_response.status,
#     cookies = {
#       'JSESSIONID': '',
#       'doc-sidebar': '300px'
#     },
#     html = splash:html(),
#   }
# end
# """

class confluenceSpider(scrapy.Spider):
  name = "confluence"
  allowed_domains = ["", ""]
  download_delay = 2
  start_urls = [
        '',
  ]
  base_url = ''
  sub_url = '/plugins/pagetree/naturalchildren.action?decorator=none&excerpt=false&sort=position&reverse=false&disableLinks=false&hasRoot=true&treeId=0&startDepth=0'
  cookies = {
    'JSESSIONID': '',
    'doc-sidebar': '300px'
  }

  def start_requests(self):  
    for url in self.start_urls:          
      yield Request(url, cookies=self.cookies) 

  def parse(self, response):
    # 首页左侧列表
    spaceList = response.css('.space-name')
    for space in spaceList:
      url = self.base_url + space.css('::attr(href)')[0].extract()
      yield scrapy.Request(url=url, callback=self.sub_space, cookies=self.cookies)

  # 拼接获取子菜单 ajax 请求
  def sub_space(self, response):
    parsed = urlparse.urlparse(response.request.url)
    pageId = urlparse.parse_qs(parsed.query)['pageId'][0]
    url = self.base_url + self.sub_url + '&pageId=' + pageId + '&ancestors=' + pageId + '&_=' + str((int(round(time.time() * 1000))))
    yield scrapy.Request(url=url, callback=self.sub_ajax_menu, cookies=self.cookies)

  def sub_ajax_menu(self, response):
    li_list = response.css('li')
    for li in li_list:
      href = li.css('div.plugin_pagetree_children_content span ::attr(href)')[0].extract()
      url = self.base_url + href
    
      logging.debug('yield url: ' + url)
      yield scrapy.Request(url=url, callback=self.parse_page, cookies=self.cookies)
      
      # 是否有子菜单
      if (len(li.css('.no-children.icon')) == 0):
        if ('pageId' in href):
          parsed = urlparse.urlparse(href)
          
          logging.debug('parse sub menu, href: ' + href)

          pageId = urlparse.parse_qs(parsed.query)['pageId'][0]
          sub_url = self.base_url + self.sub_url + '&pageId=' + pageId + '&_=' + str((int(round(time.time() * 1000))))

          logging.debug('yield url: ' + sub_url)
          yield scrapy.Request(url=sub_url, callback=self.sub_ajax_menu, cookies=self.cookies)
        else:
          urlx = self.base_url + href
          yield scrapy.Request(url=urlx, callback=self.sub_space, cookies=self.cookies)

      
  # 处理页面内容
  def parse_page(self, response):
    title = response.css('span#title-text a::text')[0].extract()
    bread_crumbs = response.css('ol#breadcrumbs a::text').extract()
    content = response.css('div#content div.wiki-content')[0].extract()

    path = ''
    for bread_crumb in bread_crumbs:
      path = path + bread_crumb + '/'

    item = ConfluenceItem()
    item['name'] = title
    item['path'] = path
    item['content'] = content

    yield item


