# -*- coding: utf-8 -*-
import scrapy,re
from ..items import  BooksItem,PythonScrapyItem

class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['www.qisuu.com']
    start_urls = ['http://www.qisuu.com/soft/sort01/']

    def parse(self, response):
        nav_list = response.css(".listBox ul li")
        for nav in nav_list:
            item = PythonScrapyItem()
            category_name = nav.css("a::text").extract_first()
            category_url = response.urljoin(nav.css("a::attr(href)").extract_first())
            item["category_name"] = category_name
            item["category_url"] = category_url
            yield item
            print(category_name)
            print(category_url)
            print("-------------------------")

        name = response.css(".listBox .tspage a").extract()
        for item in name:
            # if item.split('>')[1].split("<")[0] == '下一页':
            if re.findall(r'>(.*)</a>',item,re.S)[0] == '下一页':
                # next = item.split('"')[1]
                next = re.findall(r'"(.*)"',item,re.S)[0]
                next_url = response.urljoin(next)
                print(next_url)
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                    dont_filter=True
                )
                page = re.findall(r'_(.*).html',next,re.S)[0]
                print("已爬取至第"+page+"页")

    # def parse_books_list(self, response):
    #     href_list = response.css(".listBox ul li a::attr(href)").extract()
    #     for href in href_list:
    #         list_href = response.urljoin(href)
    #         yield scrapy.Request(
    #             url=list_href,
    #             callback=self.parse_books_list,
    #             meta=response.meta
    #         )
    #
    #     all_pages = response.css(".select[name='select'] option::attr(value)").extract()
    #     for page in all_pages:
    #         detail_url = response.urljoin(page)
    #         yield scrapy.Request(
    #             url=detail_url,
    #             callback=self.parse_books_list,
    #             meta=response.meta
    #         )
    #
    # def parse_books_detail(self, response):
    #     info_div = response.css(".info_div")
    #     title = info_div.css("h1::text").extract_first(default="")
    #     # li_list = info_div.css("ul li").extarct()
    #
    #     li_list = info_div.xpath("ul/li")
    #     size = li_list[2].xpath("text()").extract_first("")
    #     size = size.replace(u"文件大小：", "").strip()
    #     date_time = li_list[4].xpath("text()").extract_first("")
    #     date_time = date_time.replace(u"发布日期：", "").strip()
    #     user = li_list[6].xpath("a/text()").extract_first("")
    #     download_times = li_list[1].xpath("text()").extract_first("")
    #     download_times = download_times.replace(u"下载次数：", "").strip()
    #     book_degree = li_list[7].xpath("em/@class").extract_first("")
    #     book_degree = book_degree.replace("lstar", "").strip()
    #     download_url = response.xpath("//a[@class='downButton']/@href")[1].extract()
    #     img_url = response.xpath("//div[@class='detail_pic']/img/@src").extract_first("")
    #     img_url = response.urljoin(response.url, img_url)
    #     category_name = response.meta['category_name']
    #     print(title, user, date_time, category_name)
    #
    #     item = BooksItem()
    #     item['title'] = title
    #     item['size'] = size
    #     item['date_time'] = date_time
    #     item['user'] = user
    #     item['download_times'] = download_times
    #     item['book_degree'] = book_degree
    #     # 小说要以GBK格式进行存储
    #     ########################
    #     item['download_url'] = [u"%s" % download_url]
    #     item['img_url'] = [img_url]
    #     ########################注意以列表方式存储
    #     item['category_name'] = category_name
    #     yield item