# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import html2text
import os
from os.path import dirname
import errno
import requests
from confluence.items import *
import re

class ConfluencePipeline(object):
    def process_item(self, item, spider):
      if not isinstance(item, ConfluenceItem):
        return item

      fullpath = os.path.join(dirname(os.path.abspath(os.path.dirname(__file__))), "data", item['path'], item['name'] + '.md')

      if not os.path.exists(os.path.dirname(fullpath)):
        try:
          os.makedirs(os.path.dirname(fullpath))
        except OSError as exc: 
          if exc.errno != errno.EEXIST:
            raise

      # 替换 td 里的 p strong，cuz html2text 不支持
      content = item['content']
      content = re.sub(r'(<p>)(<strong>)', r'\1', content)
      content = re.sub(r'(</strong>)(</p>)', r'\2', content)
      content = re.sub(r'(<td.*?>)(<p>)', r'\1', content)
      content = re.sub(r'(</p>)(</td>)', r'\2', content)

      text_maker = html2text.HTML2Text()
      # text_maker.unifiable = True
      # text_maker.single_line_break = True
      content = text_maker.handle(content)
      with codecs.open(fullpath, 'w', encoding='utf-8') as f:
        f.write(content)

      return item

class ImgPipeline(object):
  def process_item(self, item, spider):
    if not isinstance(item, ImgItem):
        return item

    imgpath = os.path.join(dirname(os.path.abspath(os.path.dirname(__file__))), "data", item['path'], item['name'])
    with open(imgpath, 'w') as f:
      f.write(item['content'])

    return item
