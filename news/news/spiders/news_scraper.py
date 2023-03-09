import scrapy
from ..items import NewsItem

from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_playwright.page import PageMethod
from scrapy.crawler import CrawlerProcess
import re

class NewsSpider(CrawlSpider):
    name = 'news_scraper'


    start_urls = ['https://thehill.com/news/?page_num=%s/' % i for i in range(1,2)]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//article[@class='archive__item | ']/div[@class='archive__item__content']/h2/a"),callback='parse_item',follow=True),
        )

    def parse_item(self,response):
        item = NewsItem()

        articleBody = " ".join(response.xpath('//div[@class="article__text | body-copy | flow"]/p/text()').extract())
        articleTitle = response.xpath('normalize-space(//h1[@class="page-title"]/text())').extract()
        category = response.xpath('//section[@class="article__header"]//a/text()').extract()
        imageLink = response.xpath('//*[@id="page"]/div/section/article/div[2]/figure/div/img').extract()
        published_date = response.xpath('//section[contains(@class, "submitted-by")][1]/span[1]/text()').re('\d\d.\d\d.\d\d')

        # extracted_published_date = re.findall(r'\d\d.\d\d.\d\d',published_date)



        item['articleCategory'] = category[0]
        item['articleTitle'] = articleTitle[0]
        item['published_date'] = published_date[0]
        item['articleBody'] = articleBody
        item['imageLink'] = " ".join(imageLink[0].split(" ")[:2]) + "/>"


        yield item
     

    
if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            "CONCURRENT_REQUESTS": 32,
            "FEED_URI":'Products.jl',
            "FEED_FORMAT":'jsonlines',
        }
    )
    process.crawl(NewsSpider)
    process.start()


