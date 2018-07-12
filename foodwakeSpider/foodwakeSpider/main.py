#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/7/11 11:43
# @Author  : lcyanxi
# @Email   : lcyanxi.com
# @File    : main.py
# @Software: PyCharm
from scrapy import cmdline

cmdline.execute("scrapy crawl foodwake".split())
