# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyappItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    year = scrapy.Field()
    rating = scrapy.Field()
    m_score = scrapy.Field()
    votes = scrapy.Field()
