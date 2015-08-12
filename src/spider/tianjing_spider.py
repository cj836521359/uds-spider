#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'chencharles'

from __init__ import *

import sys
from spider import *
import time
import re



class tianjingSpider( spiderBase ):
    def __init__( self ):
        spiderBase.__init__( self )
        self.url_base = 'http://portal.tj.sgcc.com.cn:7778'
        print 'tianjingSpider'
        self.session = self.init_session()
        self.folder_base = u'天津'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            # 总部要闻
            'gbyw',
            #公司要闻
            'gsyw',
            #本部新闻
            'bbxw',
            #基层动态
            'jcdt',
            #媒体报道
            'mtbd',
        ]


        self.section_url_map[self.section_key[0]] = 'http://10.120.6.65:8080/site2/tj_zbyw/ZBYW_more.shtml'
        self.section_url_map[self.section_key[1]] = 'http://portal.tj.sgcc.com.cn:7778/tj_gsyw/GSYW_more.shtml'
        self.section_url_map[self.section_key[2]] = 'http://portal.tj.sgcc.com.cn:7778/tj_bbxw/BBXW_more.shtml'
        self.section_url_map[self.section_key[3]] = 'http://portal.tj.sgcc.com.cn:7778/tj_jcdt/JCDT_more.shtml'
        self.section_url_map[self.section_key[4]] = 'http://portal.tj.sgcc.com.cn:7778/tj_mtbd/MTBD_more.shtml'


        self.section_folder_map[self.section_key[0]] = u'总部要闻'
        self.section_folder_map[self.section_key[1]] = u'公司要闻'
        self.section_folder_map[self.section_key[2]] = u'本部新闻'
        self.section_folder_map[self.section_key[3]] = u'基层动态'
        self.section_folder_map[self.section_key[4]] = u'媒体报道'



    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-6] + '_' + str(page_num) + '.shtml'

            contentHtml = self.session.get(url, stream=True)
            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<td width=\"\d{2}%\"><a href="(.*?)"\s.*?>(.*?)</a>\s.*?<td\s.*?>\[(.*?)\].*?</td>'
                for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        #临时判断
                        if section_name == 'gbyw':
                            article_url = '%s%s' %('http://10.120.6.65:8080', mtFind.groups()[0])
                        else:
                            article_url = '%s%s' %(self.url_base, mtFind.groups()[0])

                    public_time = mtFind.groups()[2]
                    title = self.strip_tags(mtFind.groups()[1]).decode()
                    item = article_item(article_url, title, public_time)
                    item.set_section_name(section_name)
                    article_list.append(item)
            else:
                self.logger.error(u'没有获取到文章列表 ' + str(page_num))
        except BaseException, e:
            self.logger.error(str(e))
        finally:
            return article_list


if __name__ == '__main__':
    tianjing_spider = tianjingSpider()
    tianjing_spider.init_log(u'天津.log')
    tianjing_spider.set_save_folder_path(globalconf.save_folder['tianjing'])
    tianjing_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['tianjing']
    tianjing_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in tianjing_spider.section_key:
        tianjing_spider.logger.info(u"获取栏目:" + section_item + ":" + tianjing_spider.section_folder_map[section_item])
        for page_num in range(tianjing_spider.page_number):
            article_list = tianjing_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                tianjing_spider.stripy_article_context(item)
