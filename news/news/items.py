# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    articleCategory = scrapy.Field()
    articleTitle = scrapy.Field()
    articleBody = scrapy.Field()
    imageLink = scrapy.Field()
    published_date = scrapy.Field()
    pass
