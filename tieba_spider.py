"""
爬取百度贴吧
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
import urllib.request
import re
from spider import tool
import html.parser


class BDTB:
    def __init__(self, tie_number, see_lz=0):
        self.base_url = 'http://tieba.baidu.com/p/' + tie_number
        self.see_lz = '?see_lz=' + str(see_lz)
        self.tool = tool.Tool()
        self.file = None
        # 初始楼层
        self.floor = 1
        # 默认的标题，如果没有成功获取到标题的话则会用这个标题
        self.default_title = u"百度贴吧"

    # 传入页面，获取该页帖子
    def get_page(self, page_num):
        try:
            url = self.base_url + self.see_lz + '&pn=' + str(page_num)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            page_code = response.read().decode('UTF-8')

            return page_code
        except Exception as e:
            print('连接失败...', e)
            raise e

    # 获取标题
    def get_title(self, index_page):
        pattern = '<h3 class="core_title_txt pull-left text-overflow  ".*?>(.*?)</h3>'
        pattern = re.compile(pattern, re.S)
        result = re.search(pattern, index_page)
        if result:
            return html.unescape(result.group(1).strip())
        else:
            return None

    # 获取总计页数
    def get_page_num(self, index_page):
        pattern = '<li class="l_reply_num".*?>.*?<span class="red">(.*?)</span>页</li>'
        pattern = re.compile(pattern, re.S)
        result = re.search(pattern, index_page)
        if result:
            return result.group(1).strip()
        else:
            return None

    # 获取页面内容
    def get_content(self, page):
        pattern = '<div id="post_content_.*?>(.*?)</div>'
        pattern = re.compile(pattern, re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            content = '\n' + self.tool.replace(item) + '\n'
            contents.append(content.encode('UTF-8'))
        return contents

    def set_file_title(self, title):
        if title is not None:
            self.file = open(title + '.txt', 'w+')
        else:
            self.file = open(self.default_title + '.txt', 'w+')

    # 向文件写入内容
    def write_data(self, contents):
        for item in contents:
            # 楼层分隔符
            floor_line = "\n" + str(self.floor) + u"楼----------------------------------------------------------------\n"
            self.file.write(floor_line)
            self.file.write(str(item))
            self.floor += 1

    def start(self):
        index_page = self.get_page(1)
        page_num = self.get_page_num(index_page)
        title = self.get_title(index_page)
        self.set_file_title(title)

        if page_num is None:
            print('页面已失效...')
            return

        try:
            print('共有' + str(page_num) + '页')
            for i in range(1, int(page_num) + 1):
                print('正在写入第' + str(i) + '页数据')
                page = self.get_page(i)
                contents = self.get_content(page)
                self.write_data(contents)
        except Exception as e:
            print('写入文件异常', e)
        finally:
            print('写入完成...')


# tie_num = '4399638202'
code = input("请输入帖子代号...\n")
seeLZ = input("是否只获取楼主发言，是输入1，否输入0\n")

bdtb = BDTB(code, seeLZ)
bdtb.start()


