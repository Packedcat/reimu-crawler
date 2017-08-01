# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from crawler.items import ArticleItem


class QuotesSpider(scrapy.Spider):

    name = 'reimu'
    allow_domains = ['blog.reimu.net']
    start_urls = [
        'https://blog.reimu.net',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for next_page in response.css('a.larger::attr(href)').extract():
            if not next_page:
                continue
            yield scrapy.Request(next_page, callback=self.parse)

        for article in response.css('h2.entry-title a::attr(href)').extract():
            if not article:
                continue
            yield scrapy.Request(article, callback=self.parse_article)

    def parse_article(self, response):
        al = ItemLoader(item=ArticleItem(), response=response)
        index = response.url[::-1].index('/')
        article_id = response.url[-index:]
        al.add_value('article_id', article_id)
        al.add_css('title', 'h1.entry-title::text')
        al.add_css('target', 'div.entry-content pre')
        al.add_css('image_urls', 'div.entry-content p img::attr(src)')
        return al.load_item()
