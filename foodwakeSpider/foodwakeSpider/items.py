# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FoodwakespiderItem(scrapy.Item):
    # 食材名称
    name = scrapy.Field()
    # 食材别名
    nickname = scrapy.Field()
    # 食材详细营养成分
    info = scrapy.Field()
