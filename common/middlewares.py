# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from agents import AGENTS
import json

class ProxyMiddleware(object):
    def __init__(self):
        with open('proxy.json', 'r') as f:
            self.proxies = json.load(f)
    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://{}'.format(random.choice(self.proxies))

class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
