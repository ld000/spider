"""
爬取统计局行政区划代码, 输出 insert sql
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
import urllib.request
import re
import html.parser

# 处理页面标签类
class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()


class Location:
    def __init__(self):
        self.base_url = 'http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/' + '201703/t20170310_1471429.html'
        self.tool = Tool()
        self.file = None
        self.default_title = 'location_code'

    # 获取页面
    def get_page(self):
        try:
            url = self.base_url
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            page_code = response.read().decode('UTF-8')

            return page_code
        except Exception as e:
            print('连接失败...', e)
            raise e

    # 获取内容div
    def get_content_div(self, index_page):
        pattern = '<div class="TRS_PreAppend".*?>(.*?)</div>'
        pattern = re.compile(pattern, re.S)
        result = re.search(pattern, index_page)
        if result:
            return html.unescape(result.group(1).strip())
        else:
            return None

    # 获取所有行
    def get_p(self, page):
        pattern = '<p class="MsoNormal">(.*?)</p>'
        pattern = re.compile(pattern, re.S)
        items = re.findall(pattern, page)
        return items

    def generate_sql(self, code, name, parent_code, parent_province, parent_city):
        sql = 'INSERT INTO location(code, name, parent_code, province, city) VALUES'
        sql = (sql + '(\'' + str(code)
                                    + '\', \'' + str(name)
                                    + '\', \'' + str(parent_code)
                                    + '\', \'' + str(parent_province)
                                    + '\', \'' + str(parent_city)
                                    + '\');')
        return sql

    def get_content(self, ps):
        parent_code = 0
        parent_city = ''
        parent_province = ''
        contents = []
        sql = 'INSERT INTO location(code, name, parent_code, province, city) VALUES'

        code_pattern = '<span lang="EN-US">(.*?)<span>'
        code_pattern = re.compile(code_pattern, re.S)

        name_pattern = '<span style="font-family: 宋体">(.*?)</span>'
        name_pattern = re.compile(name_pattern, re.S)

        for p in ps:
            item = {}

            # 代码
            code_result = re.search(code_pattern, p)
            code = html.unescape(code_result.group(1).strip())

            # 名字
            name_result = re.findall(name_pattern, p)

            name = ''
            # 省, 值包含一个匹配
            if (len(name_result) == 1):
                parent_code = 0
                parent_city = ''
                parent_province = ''

                name = html.unescape(name_result[0].strip())

                contents.append(self.generate_sql(code, name, parent_code, parent_province, parent_city))
                parent_code = code
                parent_province = name

            # 市或区, 值包含两个匹配
            if (len(name_result) == 2):
                name = html.unescape(name_result[1].strip())
                if (len(name_result[0]) == 1):  # 市, 前面只有 1 个空格
                    parent_city = ''
                    contents.append(self.generate_sql(code, name, parent_code, parent_province, parent_city))
                    parent_city = name
                    parent_code = code
                else:
                    contents.append(self.generate_sql(code, name, parent_code, parent_province, parent_city))

        return contents

    def set_file_title(self):
        self.file = open(self.default_title + '.txt', 'w+')

    # 向文件写入内容
    def write_data(self, contents):
        for item in contents:
            self.file.write(str(item) + '\n')

    def start(self):
        index_page = self.get_page()
        content = self.get_content_div(index_page)
        ps = self.get_p(content)
        contents = self.get_content(ps)

        print('条数: ' + str(len(contents)))

        self.set_file_title()

        try:
            self.write_data(contents)
        except Exception as e:
            print('写入文件异常', e)
        finally:
            print('写入完成...')


location = Location()
location.start()
