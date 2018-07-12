# -*- coding: utf-8 -*-
import scrapy
from foodwakeSpider.items import FoodwakespiderItem
from bs4 import BeautifulSoup
import bs4
import time


class FoodwakeSpider(scrapy.Spider):
    name = 'foodwake'
    allowed_domains = ['www.foodwake.com']
    start_urls = ['http://www.foodwake.com/category/food-class/0']

    def parse(self, response):
        foodwake = []
        for box in response.xpath('//div[@class="row margin-b2"]'):
            for tag_as in box.xpath('.//div[@class="col"]//a'):
                foodwake.append(tag_as.xpath('.//@href').extract()[0])
                new_url = tag_as.xpath('.//@href').extract()[0]
                yield scrapy.Request(new_url, callback=self.parse_item)

    def parse_item(self, response):
        for box in response.xpath('//div[@class="row margin-b2"]'):
            for tag_as in box.xpath('.//div[@class="col"]//a'):
                new_url = tag_as.xpath('.//@href').extract()[0]
                yield scrapy.Request(new_url, callback=self.parse_item_info)

    def parse_item_info(self, response):
        item = FoodwakespiderItem()
        name = response.xpath('//h1[@class="color-yellow"]/text()').extract()[0].strip()
        food_nickname = ""
        try:
            nicknames = response.xpath('//h2[@class="h3 text-light"]/text()').extract()[0].strip()
            food_nickname = nicknames.split('：')[1]
        except:
            food_nickname = "无"
        infoList = []
        for box in response.xpath('//table[@class="table table-hover"]'):
            for tag_as in box.xpath('.//tr'):
                tds = tag_as.xpath('.//td')
                length = tag_as.xpath('.//td').extract()
                if len(length) == 3:
                    info = {}
                    td_name = tds.xpath('.//text()').extract()[0]
                    td_unit = tds.xpath('.//text()').extract()[1]
                    td_value = ""
                    #防止td为空取不到值
                    try:
                        td_value = td_unit + tds.xpath('.//text()').extract()[2]
                        info[td_name] = td_value
                    except:
                        info[td_name] = td_unit
                    infoList.append(info)
        item['name'] = name
        item['nickname'] = food_nickname
        item['info'] = infoList
        yield item
        print("休眠10s")
        time.sleep(10)
