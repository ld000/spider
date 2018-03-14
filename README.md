# spider
python 爬虫

qiushibaike_spider.py，是爬取糗事百科首页内容的

tieba_spider.py，是按楼层爬取百度贴吧帖子的

location_code_spider.py, 爬取统计局行政区划代码, 输出 insert sql

## scrapy spider

require `python2.7` `scrapy1.0+`

how to use
```
cd confluence
scrapy crawl confluence
```

### amazonsims 亚马逊 还买了什么 列表

### confluence

修改 `allowed_domains`, `start_urls`, `base_url`, `cookies` 参数

e.g
```
allowed_domains = ["www.confluence.com"]
start_urls = [
      'http://www.confluence.com/dashboard.action',
]
base_url = 'http://www.confluence.com'
cookies = {
  'JSESSIONID': '338CACC64F0C6C9CA88550EAB7978674',
  'doc-sidebar': '300px'
}
```

`JSESSIONID` 为登录后 cookies 里的 sessionId，这里简单处理了，没有实现页面登录，有需要的自己实现下


