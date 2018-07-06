# -*- coding: utf-8 -*-
from scrapy import Spider,Request
import re
from ..items import BooksItem


class BookspiderSpider(Spider):
    name = 'bookspider'
    allowed_domains = ['www.qisuu.com']
    start_urls = ['http://www.qisuu.com/soft/sort01/']

    def parse(self, response):
        book_list = response.css(".listBox ul li")
        for book in book_list:
            # item = BooksItem()
            title = book.css("a::text").extract_first()
            book_url = response.urljoin(book.css("a::attr(href)").extract_first())
            img_url = response.urljoin(book.css("a img::attr(src)").extract_first())
            # item["title"] = title
            # item["book_url"] = book_url
            # item["img_url"] = img_url
            print(title)
            print(book_url)
            print("-------------------------")

            yield Request(
                url=book_url,
                callback=self.parse_detail,
                meta={"title": title,"book_url":book_url,"img_url":img_url},
                dont_filter=True
            )

            # yield item


        name = response.css(".listBox .tspage a").extract()
        for item in name:
            # if item.split('>')[1].split("<")[0] == '下一页':
            if re.findall(r'>(.*)</a>',item,re.S)[0] == '下一页':
                # next = item.split('"')[1]
                next = re.findall(r'"(.*)"',item,re.S)[0]
                next_url = response.urljoin(next)
                print(next_url)
                yield Request(
                    url=next_url,
                    callback=self.parse,
                    dont_filter=True
                )
                page = re.findall(r'_(.*).html',next,re.S)[0]
                print("已爬取至第"+page+"页")

    def parse_detail(self, response):
        book_detail = response.css(".detail_right ul li")
        click_count= book_detail[0].css("::text").extract_first().split("：")[1]
        book_size = book_detail[1].css("::text").extract_first().split("：")[1]
        update_time = book_detail[3].css("::text").extract_first().split("：")[1]
        update_status = book_detail[4].css("::text").extract_first().split("：")[1]
        author = book_detail[5].css("::text").extract_first().split("：")[1]
        show_info = response.css(".showInfo p::text").extract_first()
        download_url = response.css(".showDown ul li").extract()[2].split("','")[1]
        item = BooksItem()
        item["title"] = response.meta["title"]
        item["book_url"] = response.meta["book_url"]
        item["img_url"] = response.meta["img_url"]
        item["click_count"] = click_count
        item["book_size"] = book_size
        item["update_time"] = update_time
        item["update_status"] = update_status
        item["author"] = author
        item["show_info"] = show_info
        item["download_url"] = download_url
        print(response.meta)
        yield item


