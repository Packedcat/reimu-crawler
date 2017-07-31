# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):

    title = scrapy.Field()
    image_urls = scrapy.Field()
    target = scrapy.Field()


class ImageItem(scrapy.Item):

    images = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
