# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from crawler.items import ImageItem


class QuotesSpider(scrapy.Spider):

    name = 'reimu'
    allow_domains = ['blog.reimu.net']
    start_urls = [
        'https://blog.reimu.net',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # 请求下一页scrapy.Request(next_page, callback=self.parse)
    # 请求文章本体scrapy.Request(article, callback=self.parse_article)
    # 解析图片yield self.parse_item(response)
    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        yield self.parse_item(response)
        # <h2 class="entry-title"><a href="https://blog.reimu.net/archives/10309" rel="bookmark">御所动态</a></h2>
        for next_page in response.css('a.larger::attr(href)').extract():
            # 防止空值报错
            if not next_page:
                continue
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        # for article in response.css('article.hentry'):
        #     img = article.css('div.entry-content').css('img')
        #     yield {
        #         'title': article.css('h2.entry-title').css('a::text').extract_first(),
        #         'link':  article.css('h2.entry-title').css('a::attr(href)').extract(),
        #         'image': len(img) > 0 and img.re(r'src="(.*?)"')[0] or None,
        #     }

    def parse_item(self, response):
        il = ItemLoader(item=ImageItem(), response=response)
        il.add_css('image_urls', 'img::attr(src)')
        return il.load_item()

    # 解析文章页面
    # 返回描述图片以及pre里面的内容
    def parse_article(self, response):
        yield self.parse_item(response)
        return