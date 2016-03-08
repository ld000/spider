"""
爬取糗事百科首页
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
import urllib.request
import re


# 糗事百科爬虫类
class QSBK:
    def __init__(self):
        self.pageIndex = 1
        # 初始化 header
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.header = {'User-Agent': self.user_agent}
        # 存放段子的变量
        self.stories = []
        # 程序是否运行
        self.enable = False

    # 传入索引，获得某页代码
    def get_page(self, page_index):
        print('加载页面...')
        try:
            url = 'http://www.qiushibaike.com/8hr/page/' + str(page_index)
            request = urllib.request.Request(url, headers=self.header)
            response = urllib.request.urlopen(request)
            page_code = response.read().decode('UTF-8')
            print('加载成功...')

            return page_code
        except Exception as e:
            print('加载页面失败...', e)

    # 传入某一页代码，获得本页不带图片的段子列表
    def get_page_items(self, page_index):
        page_code = self.get_page(page_index)
        if not page_code:
            return None

        page_stores = []

        pattern = '<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>.*?<h2>(.*?)</h2>.*?</a>.*?' \
                  '<div.*?class="content".*?>(.*?)</div>.*?' \
                  '<div.*?class="stats.*?class="number">(.*?)</i>'
        pattern = re.compile(pattern, re.S)
        items = re.findall(pattern, page_code)
        for item in items:
            have_img = re.search('img', item[1])
            if not have_img:
                page_stores.append([item[0].strip(), item[1].strip(), item[2].strip()])

        return page_stores

    # 加载并提取页面内容，加入列表
    def load_page(self):
        if self.enable:
            # 如果未看的页数少于两页，则再加载一页
            if len(self.stories) < 2:
                page_stores = self.get_page_items(self.pageIndex)
                if page_stores:
                    self.stories.append(page_stores)
                    # 获取完之后索引加一
                    self.pageIndex += 1

    # 每次回车打印一个段子
    def get_one_story(self, page_stories, page):
        for story in page_stories:
            input_code = input()
            self.load_page()
            if input_code == 'Q':
                self.enable = False
                return
            print("第%d页\t发布人:%s\n%s\n赞:%s\n" % (page, story[0], story[1], story[2]))

    # 开始方法
    def start(self):
        print(u"正在读取糗事百科,按回车查看新段子，Q退出")
        self.enable = True
        self.load_page()
        now_page = 0
        while self.enable:
            if len(self.stories) > 0:
                page_stories = self.stories[0]
                now_page += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                self.get_one_story(page_stories, now_page)

spider = QSBK()
spider.start()

