# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'

import globalconf
import demjson
import sys

from fujian_spider import  *
from spider_factory import *
import os

if __name__ == '__main__':
    json_dic = demjson.decode(globalconf.str)
    fac = spiderFactory()
    # 遍历各个网省,进行爬取
    for province_item in json_dic['provinces']:
        if province_item['need_spider'] == True:
            spider = fac.factory(province_item['key'])
            print u'爬取 ' + province_item['name']
            strtitle = 'title ' + province_item['key']
            os.system(strtitle)
            # 获取各个网省的栏目列表
            section_lst = [section for section in province_item['sections'] if section[section['id']]['spider'] == True]
            lst = []
            for sec in section_lst:
                lst.append(sec['id'])
            # 进行爬取信息设置
            ll = spider.set_section_list(lst)
            spider.init_log(province_item['logname'])
            spider.set_save_folder_path(province_item['save_path']) # 保存保存的文件路径
            spider.init_mkdir_folder()
            # 设置爬取的时间限制,例如从2015-04-01~2015-05-01
            str_limit_date = province_item['limit_date']
            spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])


            # 爬取文章列表和文章内容
            for section_item in ll:
                spider.logger.info(u"获取栏目:" + section_item + ":" + spider.section_folder_map[section_item])
                for page_num in range(spider.page_number):
                    print page_num
                    article_list = spider.stripy_article_list(section_item, page_num)
                    for item in article_list:
                        spider.stripy_article_context(item)




