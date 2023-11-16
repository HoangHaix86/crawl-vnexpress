import sqlite3
from scrapy.spiders import CrawlSpider, Rule, Response
from scrapy.linkextractors import LinkExtractor

class VNExpressSpider(CrawlSpider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["https://vnexpress.net"]

    custom_settings = {
        "CONCURRENT_ITEMS": 30,
        "CONCURRENT_REQUESTS": 30,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 30,
        "DEPTH_PRIORITY" : 1 ,
        "SCHEDULER_DISK_QUEUE" : 'scrapy.squeues.PickleFifoDiskQueue',
        "SCHEDULER_MEMORY_QUEUE" : 'scrapy.squeues.FifoMemoryQueue'
    }

    rules = [
        Rule(
            link_extractor=LinkExtractor(
                allow=("^https:\/\/vnexpress\.net\/.+\.html$", "^https:\/\/vnexpress\.net\/.+"),
                tags=("a"),
                attrs=("href"),
                unique=True,
                ),
                callback="parse_item",
                follow=True
            )
    ]
    
    conn = sqlite3.connect('/content/drive/MyDrive/data.db')
    c = conn.cursor()
    
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.c.execute("CREATE TABLE IF NOT EXISTS data (url TEXT, title TEXT, content TEXT)")

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
         
            self.c.execute("INSERT INTO data VALUES (?, ?, ?)", (response.url, f"{_type}", f"{_title_detail} {_description} {_content}"))
            self.conn.commit()
        except Exception as e:
            pass
