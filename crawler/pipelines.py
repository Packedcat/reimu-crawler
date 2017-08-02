# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class CaptionPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url.strip())

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        path = '%s/%s' % (self.store.basedir, item['title'][0])
        if not os.path.exists(path):
            os.makedirs(path)
        for image_path in image_paths:
            src_dir = '%s/%s' % (self.store.basedir, image_path)
            dst_dir = '%s/%s' % (path, image_path[4:])
            os.rename(src_dir, dst_dir)
        # TODO splice path if have else pipeline
        item['image_paths'] = image_paths
        return item


class DescriptionPipeline(object):

    def process_item(self, item, spider):
        base_path = spider.settings.get('IMAGES_STORE')
        save_path = '%s/%s' % (base_path, item['title'][0])
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        content = item.get('target')
        if content:
            with open('%s/link.txt' % save_path, 'wb') as f:
                f.write(content[0].encode('utf-8'))
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item
