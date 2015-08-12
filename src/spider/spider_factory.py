#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from src.common_utils import common_utils

__author__ = 'chencharles'

from __init__ import *
import requests
import re
import sys
import os

from anhui_spider import *
from beijing_spider import *
from chongqing_spider import *
from fujian_spider import *
from gansu_spider import *
from hebei_spider import *
from heilongjiang_spider import *
from henan_spider import *
from hubei_spider import *
from hunan_spider import *
from jiangsu_spider import *
from jiangxi_spider import *
from jibei_spider import *
from jilin_spider import *
from kefu_spider import *
from liaoning_spider import *
from neimenggu_spider import *
from ningxia_spider import *
from qinghai_spider import *
from shaanxi_spider import *
from shandong_spider import *
from shanghai_spider import *
from shanxi_spider import *
from sichuan_spider import *
from tianjing_spider import *
from xinjiang_spider import *
from xintong_spider import *
from xizang_spider import *
from zhejiang_spider import *


class spiderFactory():

    def __init__(self):
        pass

    def factory(self, which):

        if which == 'anhui':
            return anhuiSpider()
        elif which == 'beijing':
            return beijingSpider()
        elif which == 'chongqing':
            return chongqingSpider()
        elif which == 'fujian':
            return fujianSpider()
        elif which == 'gansu':
            return gansuSpider()
        elif which == 'hebei':
            return hebeiSpider()
        elif which == 'heilongjiang':
            return heilongjiangSpider()
        elif which == 'henan':
            return henanSpider()
        elif which == 'hubei':
            return hubeiSpider()
        elif which == 'hunan':
            return hunanSpider()
        elif which == 'jiangsu':
            return jiangsuSpider()
        elif which == 'jiangxi':
            return jiangxiSpider()
        elif which == 'jibei':
            return jibeiSpider()
        elif which == 'jilin':
            return jilinSpider()
        elif which == 'kefu':
            return kefuSpider()
        elif which == 'liaoning':
            return liaoningSpider()
        elif which == 'neimenggu':
            return neimengguSpider()
        elif which == 'ningxia':
            return ningxiaSpider()
        elif which == 'qinghai':
            return qinghaiSpider()
        elif which == 'shaanxi':
            return shaanxiSpider()
        elif which == 'shandong':
            return shandongSpider()
        elif which == 'shanghai':
            return shanghaiSpider()
        elif which == 'shanxi':
            return shanxiSpider()
        elif which == 'sichuan':
            return sichuanSpider()
        elif which == 'tianjing':
            return tianjingSpider()
        elif which == 'xinjiang':
            return xinjiangSpider()
        elif which == 'xintong':
            return xintongSpider()
        elif which == 'xizang':
            return xizangSpider()
        elif which == 'zhejiang':
            return zhejiangSpider()
        else:
            return None