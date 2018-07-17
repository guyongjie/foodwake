# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from foodwakeSpider.user_agent import USER_AGENT_LIST


# setting 里设置   'foodwakeSpider.middlewares.UserAgentMiddleware': 300,
class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(USER_AGENT_LIST)
        request.headers["User-Agent"] = agent
