#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import logging
import time
from urllib import request, parse, error

class reimuSpider(object):
    name = 'reimu'

    def __init__(self):
        self.enable = False
        self.page_index = 1
        self.base_url = 'https://blog.reimu.net/'
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        self.headers = { 'User-Agent' : self.user_agent }
        self.articles = []

    def getPage(self, page_index):
        try:
            # TODO: index判断
            url = self.base_url + 'page/'+ str(page_index)
            data = { '_': int(time.time()) }
            data = parse.urlencode(data).encode('utf-8')
            req = request.Request(url, data=data, headers=self.headers)
            response = request.urlopen(req)
            return response.read().decode('utf-8')
        except error.HTTPError as e:
            logging.exception(e)
            return None

    def getPageItems(self, page_index):
        page_code = self.getPage(page_index)
        if not page_code:
            logging.warning('页面加载失败....')
            return None
        print('页面%s加载成功....' % page_index)
        articles = []
        pattern = re.compile(r'<article.*?entry-title">.*?href="(.*?)".*?bookmark">(.*?)</a>.*?</article>', re.DOTALL)
        items = re.findall(pattern, page_code)
        for item in items:
            articles.append('链接：%s，标题：%s' % (item[0], item[1]))
        return articles

    def loadPage(self):
        if self.enable == True:
            if len(self.articles) < 2:
                articles = self.getPageItems(self.page_index)
                if articles:
                    self.articles.append(articles)
                    self.page_index += 1

    def getOneArticle(self, article):
        for article in articles:
            print(article)

    def start(self):
        print('呜呜呜～')
        self.enable = True
        self.loadPage()
        now_page = 0
        while self.enable:
            if len(self.articles) > 0:
                article = self.articles[0]
                now_page += 1
                del self.articles[0]
                self.getOneArticle(article)


spider = reimuSpider()
spider.start()
