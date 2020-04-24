# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VdgeospiderItem(scrapy.Item):
    # define the fields for your item here like:
    collection = table = 'dict_geo'
    name = scrapy.Field()
    parent = scrapy.Field()
    sname = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    type = scrapy.Field()
    pass
