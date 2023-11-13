import sqlite3
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Response
from scrapy.linkextractors import LinkExtractor

from VNExpress.items import VnexpressItem

class VNExpressSpider(CrawlSpider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["https://vnexpress.net"]

    custom_settings = {
        "CONCURRENT_ITEMS": 40,
        "CONCURRENT_REQUESTS": 20,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 20,
        "DEPTH_PRIORITY" : 1 ,
        "SCHEDULER_DISK_QUEUE" : 'scrapy.squeues.PickleFifoDiskQueue',
        "SCHEDULER_MEMORY_QUEUE" : 'scrapy.squeues.FifoMemoryQueue'
    }

    rules = [
        Rule(
            link_extractor=LinkExtractor(
                allow=("^https:\/\/vnexpress\.net\/.+\.html$"),
                tags=("a"),
                attrs=("href"),
                unique=True,
                ),
                callback="parse_item",
                follow=True
            )
    ]
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.c.execute("CREATE TABLE IF NOT EXISTS data (url TEXT PRIMARY KEY, title TEXT, content TEXT)")

    @staticmethod
    def process_breadcrumb(value):
        return value not in ["\n", "\t"]
            


    def parse_item(self, response: Response):
        try:
            _type = " | ".join(filter(self.process_breadcrumb, response.css(".breadcrumb ::text").getall()))
            if not _type:
                raise Exception
            _title_detail = response.css(".title-detail::text").get()
            _description = response.css(".description::text").get()
            _content = " ".join(" ".join(response.css(".fck_detail ::text").getall()).split())
         
            item = VnexpressItem()
            item["url"] = response.url
            item["title"] = f"{_type}"
            item["content"] = f"{_title_detail} {_description} {_content}"
            
            self.c.execute("INSERT INTO data VALUES (?, ?, ?)", (item["url"], item["title"], item["content"]))
            self.conn.commit()
            
            return item
        except Exception as e:
            pass
