import scrapy
from scrapy.spiders import CrawlSpider, Rule, Response
from scrapy.linkextractors import LinkExtractor

from VNExpress.items import VnexpressItem

class VNExpressSpider(CrawlSpider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["https://vnexpress.net"]

    custom_settings = {
        "CONCURRENT_ITEMS": 20,
        "CONCURRENT_REQUESTS": 10,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 10,
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
            return item
        except Exception as e:
            pass