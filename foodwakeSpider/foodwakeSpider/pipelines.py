# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from scrapy import log
from twisted.enterprise import adbapi


# 把数据生成json数据
class FoodwakespiderPipeline(object):
    def __init__(self):
        # 打开文件
        self.file = open('data.json', 'w', encoding='utf-8')

    # 该方法用于处理数据
    def process_item(self, item, spider):
        # 读取item中的数据
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 写入文件
        self.file.write(line)
        # 返回item
        return item

    # 该方法在spider被开启时被调用。
    def open_spider(self, spider):
        pass

    # 该方法在spider被关闭时被调用。
    def close_spider(self, spider):
        pass


# 将爬取到的信息插入到MySQL数据库中
class DbScrapyPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._conditional_insert, item, spider)  # 调用插入的方法
        log.msg("-------------------连接好了-------------------")
        d.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        d.addBoth(lambda _: item)
        return d

    def _conditional_insert(self, conn, item, spider):
        log.msg("-------------------打印-------------------")
        print(item['info'])
        sql = "insert into foodwake (name, nickname,info,url) values(%s, %s, %s,%s)"
        params = (item['name'], item['nickname'], item['info'], item['url'])
        conn.execute(sql, params)
        log.msg("-------------------一轮循环完毕-------------------")

    def _handle_error(self, failue, item, spider):
        print(failue)
