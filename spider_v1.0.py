#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
import urllib.request
import re

from collections import deque

queue = deque() # 要爬取页面的队列
visited = set() # 以访问过的页面

url = 'http://news.dbanotes.net'

queue.append(url)
cnt = 0

while queue:
    url = queue.popleft()   # 队首出队列
    visited |= {url}    # 标记为已访问

    print('已经抓取：' + str(cnt) + '     正在抓取 <--- ' + url)
    cnt += 1

    try:
        urlop = urllib.request.urlopen(url, timeout=3)
        if 'html' not in urlop.getheader('Content-Type'):
            continue
        data = urlop.read().decode('UTF-8')
    except Exception as e:
        print(e)
        continue

    linkre = re.compile('href=\"(.+?)\"')
    for x in linkre.findall(data):
        if 'http' in x and x not in visited:
            queue.append(x)
            print('加入队列 --->  ' + x)
