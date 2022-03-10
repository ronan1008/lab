import scrapy
from scrapy.exceptions import CloseSpider

class PttSpider(scrapy.Spider):
    count_page = 1
    name = 'ptt'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/movie/index.html']
    def parse(self, response):
        for q in response.css('div.r-ent'):
            item = {
                'push':q.css('div.nrec > span.hl::text').extract_first(),
                'title':q.css('div.title > a::text').extract_first(),
                'href':q.css('div.title > a::attr(href)').extract_first(),
                'date':q.css('div.meta > div.date::text').extract_first(),
                'author':q.css('div.meta > div.author::text').extract_first()
            }
            yield(item)
        next_page_url = response.css('div.action-bar > div.btn-group > a.btn::attr(href)')[3].extract()
        print(f"{next_page_url}, {self.count_page} .............")
        if next_page_url and self.count_page <= 10:
            self.count_page = self.count_page + 1
            newurl = response.urljoin(next_page_url)
        else:
            raise CloseSpider('close it')
        yield scrapy.Request(newurl, callback=self.parse, dont_filter=True)
