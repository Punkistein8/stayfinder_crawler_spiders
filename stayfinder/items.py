# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZzItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nombreHotel = scrapy.Field()
    estrellas = scrapy.Field()
    pass  # pass is a placeholder for future code
