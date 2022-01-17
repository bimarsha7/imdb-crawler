# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    imdbId   = scrapy.Field()
    title    = scrapy.Field()
    title_metadata = scrapy.Field()
    top_cast = scrapy.Field()
    director = scrapy.Field()
    genre    = scrapy.Field()
    taglines = scrapy.Field()
    plot     = scrapy.Field()
    plot_keywords = scrapy.Field()

