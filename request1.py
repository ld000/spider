'''
模拟请求
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib
import urllib.request

data = {}
data['word'] = 'Jecvay Notes'

url_value = urllib.parse.urlencode(data)
print(url_value)
url = "http://www.baidu.com/s?"
full_url = url + url_value

data = urllib.request.urlopen(full_url).read()
# data = data.decode('UTF-8')
print(data)
