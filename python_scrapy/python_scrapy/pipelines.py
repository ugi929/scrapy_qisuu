# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline,FilesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import logging,json

# class PythonScrapyPipeline(object):
#     def process_item(self, item, spider):
#         return item

# 修改logging的名字
logging1 = logging.getLogger('SaveImgPipeline')
class ImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield Request(url=item['img_url'],meta={"title":item["title"]})

    def item_completed(self, results, item, info):
        if not results[0][0]:
            raise DropItem('下载失败')
        logging1.debug('下载完成')
        return item

    def file_path(self, request, response=None, info=None):
        filename = request.meta["title"]+ "." + request.url.split('/')[-1].split('.')[-1]
        return filename

logging2 = logging.getLogger('SaveFilePipeline')
class FilePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        yield Request(url=item['download_url'],meta={"title":item["title"]})

    def item_completed(self, results, item, info):
        if not results[0][0]:
            raise DropItem('下载失败')
        logging2.debug('下载完成')
        return item

    def file_path(self, request, response=None, info=None):
        filename = request.meta["title"]+ "." + request.url.split('/')[-1].split('.')[-1]
        return filename


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.filename = open("books.json", "wb")

    def process_item(self, item, spider):
        jsontext = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.filename.write(jsontext.encode("utf-8"))
        return item

    def close_spider(self, spider):
        self.filename.close()