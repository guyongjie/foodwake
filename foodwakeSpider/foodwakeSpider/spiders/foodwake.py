# -*- coding: utf-8 -*-
import scrapy
from foodwakeSpider.items import FoodwakespiderItem
import random
import time


class FoodwakeSpider(scrapy.Spider):
    name = 'foodwake'
    allowed_domains = ['www.foodwake.com']
    start_urls = ['http://www.foodwake.com/category/food-class/0']

    def parse(self, response):
        for box in response.xpath('//div[@class="row margin-b2"]//a'):
            new_url = box.xpath('.//@href').extract()[0]
            yield scrapy.Request(new_url, callback=self.parse_item)

    def parse_item(self, response):
        for box in response.xpath('//div[@class="row margin-b2"]//a'):
            new_url = box.xpath('.//@href').extract()[0]
            yield scrapy.Request(new_url, meta={"url": new_url}, callback=self.parse_item_info)

    def parse_item_info(self, response):
        item = FoodwakespiderItem()
        url = response.meta["url"]
        name = response.xpath('//h1[@class="color-yellow"]/text()').extract()[0].strip()
        food_nickname = ""
        try:
            nicknames = response.xpath('//h2[@class="h3 text-light"]/text()').extract()[0].strip()
            food_nickname = nicknames.split('：')[1]
        except:
            food_nickname = "无"
        infoList = []
        for box in response.xpath('//table[@class="table table-hover"]//tr'):
            tds = box.xpath('.//td')
            if len(tds) == 3:
                info = {}
                td_name = tds.xpath('.//text()').extract()[0]
                td_unit = tds.xpath('.//text()').extract()[1]
                td_value = ""
                # 防止td为空取不到值
                try:
                    td_value = td_unit + tds.xpath('.//text()').extract()[2]
                    info[td_name] = td_value
                except:
                    info[td_name] = td_unit
                infoList.append(info)
        item['url'] = url
        item['name'] = name
        item['nickname'] = food_nickname
        item['info'] = str(infoList)
        yield item
        print("休眠1到10s之间产生一个随机数")
        time.sleep(random.randint(1, 15))
