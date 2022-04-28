import scrapy
from scrapy.exceptions import CloseSpider
from ..items import MyfirstItem

class PttSpider(scrapy.Spider):
    count_page = 1
    name = 'ptt'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/movie/index.html']
    def parse(self, response):
        items = MyfirstItem()
        for q in response.css('div.r-ent'):
            items['push'] = q.css('div.nrec > span.hl::text').extract_first()
            items['title'] = q.css('div.title > a::text').extract_first()
            items['href'] = q.css('div.title > a::attr(href)').extract_first()
            items['date'] = q.css('div.meta > div.date::text').extract_first()
            items['author'] = q.css('div.meta > div.author::text').extract_first()
            yield(items)
        next_page_url = response.css('div.action-bar > div.btn-group > a.btn::attr(href)')[3].extract()
        print(f"{next_page_url}, {self.count_page} .............")
        if next_page_url and self.count_page <= 10:
            self.count_page = self.count_page + 1
            newurl = response.urljoin(next_page_url)
            yield scrapy.Request(newurl, callback=self.parse, dont_filter=True)
        else:
            return
            # raise CloseSpider('close it')
