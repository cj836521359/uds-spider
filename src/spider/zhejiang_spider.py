# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
import urllib


class zhejiangSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        # self.logger = login.initLog('zj.log')
        print 'zhejiangSpider'
        self.session = self.init_session()
        self.folder_base = u'浙江'


        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            # 国网要闻
            'gwyw',
            # 公司要闻
            'gsyw',
            # 本部新闻
            'bbxw',
            # 媒体报道
            'mtbd',
            # 基层动态
            'jcdt',
            # 图片新闻
            'tpxx',
        ]


        self.section_url_map[self.section_key[0]] = 'http://www1.zj.sgcc.com.cn/gy2015/'
        self.section_url_map[self.section_key[1]] = 'http://www1.zj.sgcc.com.cn/yw/'
        self.section_url_map[self.section_key[2]] = 'http://www1.zj.sgcc.com.cn/bbxw/'
        self.section_url_map[self.section_key[3]] = 'http://www1.zj.sgcc.com.cn/mtbd/'
        self.section_url_map[self.section_key[4]] = 'http://www1.zj.sgcc.com.cn/jcdt/'
        self.section_url_map[self.section_key[5]] = 'http://www1.zj.sgcc.com.cn/tpxw/'

        # 国网要闻
        self.section_folder_map[self.section_key[0]] = u'国网要闻'
        # 公司要闻
        self.section_folder_map[self.section_key[1]] = u'公司要闻'
        # 本部新闻
        self.section_folder_map[self.section_key[2]] = u'本部新闻'
        # 媒体报道
        self.section_folder_map[self.section_key[3]] = u'媒体报道'
        # 基层动态
        self.section_folder_map[self.section_key[4]] = u'基层动态'
        # 图片新闻
        self.section_folder_map[self.section_key[5]] = u'图片新闻'




    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        self.cur_page = page_num
        article_list = []
        if page_num == 0:
            url = self.section_url_map[section_name]
        else:
            url = self.section_url_map[section_name] + 'index_' + str(self.cur_page) + '.htm'

        contentHtml = self.session.get( url, stream=True )
        encoding = chardet.detect(contentHtml.content)['encoding']

        if contentHtml.status_code == requests.codes.ok:
            pattern = r'[^>]<a href="(.*?)" .*?class=home_title_02>(.*?)</a>\s.*?<FONT\s.*?>(.*?)</FONT></td>'
            for mtFind in re.finditer( pattern ,contentHtml.content,re.S ):
                if mtFind.groups()[0][0:4] == "http":
                    article_url = mtFind.groups()[0]
                else:
                    article_url = self.section_url_map[section_name][0:-1] + mtFind.groups()[0][1:]

                public_time = self.strip_tags(mtFind.groups()[2])
                title = mtFind.groups()[1].decode(encoding)

                item = article_item( article_url,title, public_time )
                item.set_section_name( section_name )
                article_list.append( item )
        else:
            self.logger.error(u'没有获取到文章列表 ' + str(page_num))
        return article_list



if __name__ == '__main__':
    zhejiang_spider = zhejiangSpider()
    zhejiang_spider.init_log(u'浙江.log')
    zhejiang_spider.set_save_folder_path(globalconf.save_folder['zhejiang'])
    zhejiang_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['zhejiang']
    zhejiang_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in zhejiang_spider.section_key:
        zhejiang_spider.logger.info(u"获取栏目:" + section_item + ":" + zhejiang_spider.section_folder_map[section_item])
        for page_num in range(zhejiang_spider.page_number):
            article_list = zhejiang_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                zhejiang_spider.stripy_article_context(item)














