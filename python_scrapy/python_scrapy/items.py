# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class PythonScrapyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category_name = Field()
    category_url = Field()

class BooksItem(Item):
    title = Field()
    book_url = Field()
    img_url = Field()
    click_count = Field()
    book_size = Field()
    update_time = Field()
    update_status = Field()
    author = Field()
    show_info = Field()
    download_url=Field()
