#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'chencharles'


#import spider
from __init__ import *
from spider import *
import time


class hebeiSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = 'http://portal.he.sgcc.com.cn'
        # self.logger = login.initLog('hb.log')
        print 'hbSpidder'
        self.session = self.init_session()
        self.folder_base = u'河北'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            # 国网速递
            'gwsd',
            # 公司要闻
            'gsyw',
            # 公司新闻
            'gsxw',
            # 基层动态
            'jcdt',
            #媒体报道
            'mtbd',
            # 图片新闻
            'tpxw',
            ]


        self.section_url_map[self.section_key[0]] = 'http://portal.he.sgcc.com.cn/hbucm/gsxw/gwsd/index.shtml'
        self.section_url_map[self.section_key[1]] = 'http://portal.he.sgcc.com.cn/hbucm/gsxw/gsyw/index.shtml'
        self.section_url_map[self.section_key[2]] = 'http://portal.he.sgcc.com.cn/hbucm/gsxw/bbxw/index.shtml'
        self.section_url_map[self.section_key[3]] = 'http://portal.he.sgcc.com.cn/hbucm/jcdt/index.shtml'
        self.section_url_map[self.section_key[4]] = 'http://portal.he.sgcc.com.cn/hbucm/gsxw/mtbd/index.shtml'
        self.section_url_map[self.section_key[5]] = 'http://portal.he.sgcc.com.cn/hbucm/gsxw/tpxw/index.shtml'


        # 国网速递
        self.section_folder_map[self.section_key[0]] = u'国网速递'
        # 公司要闻
        self.section_folder_map[self.section_key[1]] = u'公司要闻'
        # 公司新闻
        self.section_folder_map[self.section_key[2]] = u'公司新闻'
        # 基层动态
        self.section_folder_map[self.section_key[3]] = u'基层动态'
        # 媒体报道
        self.section_folder_map[self.section_key[4]] = u'媒体报道'
        # 图片新闻
        self.section_folder_map[self.section_key[5]] = u'图片新闻'



    #爬取文章列表
    def stripy_article_list( self, section_name, page_num ):
        self.cur_page = page_num
        article_list = []
        contentHtml = None
        if page_num == 0:
            url = self.section_url_map[section_name]
        else:
            url = self.section_url_map[section_name][0:-6] + '_' + str(page_num) + '.shtml'

        contentHtml = self.session.get(url, stream=True)
        if contentHtml.status_code == requests.codes.ok:
            pattern = r'<div class="right_list_text".*?<a href="(.*?)".*?>(.*?)</a></div>\s*?<div\s.*?\[(.*?)\]'
            for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                if mtFind.groups()[0][0:4] == "http":
                    article_url = mtFind.groups()[0]
                else:
                    article_url = '%s%s' %(self.url_base, mtFind.groups()[0])

                public_time = mtFind.groups()[2]
                #title = mtFind.groups()[1].strip('</a>').decode() #网页中包含了2个</a>
                title = self.strip_tags(mtFind.groups()[1]).decode()
                item = article_item(article_url, title, public_time)
                item.set_section_name(section_name)
                article_list.append(item)
        else:
            self.logger.error(u'没有获取到文章列表 ' + str(page_num))
        return article_list


if __name__ == '__main__':

    hebei_spider = hebeiSpider()
    hebei_spider.init_log(u'河北.log')
    hebei_spider.set_save_folder_path(globalconf.save_folder['hebei'])
    hebei_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['hebei']
    hebei_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])

    for section_item in hebei_spider.section_key:
        hebei_spider.logger.info(u"获取栏目:" + section_item + ":" + hebei_spider.section_folder_map[section_item])
        for page_num in range(hebei_spider.page_number):
            article_list = hebei_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                hebei_spider.stripy_article_context(item)

