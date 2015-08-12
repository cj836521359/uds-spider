#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'chencharles'

from __init__ import *


from spider import *
import demjson
import time
import chardet
import urllib
from src.spider.article_item import article_item


class beijingSpider( spiderBase ):
    def __init__( self ):
        spiderBase.__init__( self )
        self.url_base = ''
        # self.logger = login.initLog('bj.log')
        print 'bjSpider'
        self.session = self.init_session()
        self.folder_base = u'北京'
        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}

        self.section_key = [
            # 公司要闻
            'gsyw',
            # 本部新闻
            'bbxw',
            # 媒体报道
            'mtbd',
            # 基层动态
            'jcdt',
            # 最新通知
            'zxtz',
            ]




        # 公司要闻
        self.section_url_map[self.section_key[0]] = 'http://portal.bj.sgcc.com.cn/html/bj_main/col2510/column_2510_1.html'
        # 本部新闻
        self.section_url_map[self.section_key[1]] = 'http://portal.bj.sgcc.com.cn/html/bj_main/col2534/column_2534_1.html'
        # 媒体报道
        self.section_url_map[self.section_key[2]] = 'http://portal.bj.sgcc.com.cn/html/bj_main/col2535/column_2535_1.html'
        # 基层动态
        self.section_url_map[self.section_key[3]] = 'http://portal.bj.sgcc.com.cn/html/bj_main/col2511/column_2511_1.html'
        # 最新通知
        self.section_url_map[self.section_key[4]] = 'http://portal.bj.sgcc.com.cn/html/bj_main/col2533/column_2533_1.html'


        self.section_folder_map[self.section_key[0]] = u'公司要闻'
        self.section_folder_map[self.section_key[1]] = u'本部新闻'
        self.section_folder_map[self.section_key[2]] = u'媒体报道'
        self.section_folder_map[self.section_key[3]] = u'基层动态'
        self.section_folder_map[self.section_key[4]] = u'最新通知'

        # self.init_mkdir_folder()



    #爬取文章列表
    def stripy_article_list( self, section_name, page_num ):
        try:
            self.cur_page = page_num
            article_list = []
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-6] +  str(self.cur_page) + '.html'
                #nPos = self.section_url_map[section_name].index('nowPage=')
                #url = self.section_url_map[section_name][0:nPos] + 'nowPage=' + str( self.cur_page ) + self.section_url_map[section_name][nPos+len('nowPage=')+1:]
            print url
            # sys.exit(1)


            contentHtml = self.session.get(url, stream=True)
            encoding = chardet.detect(contentHtml.content)['encoding']

            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<td width="80%"  class="align_L"><a ><A href=\'(.*?)\'.*?>(.*?)</A></a></td>\s.*?<td.*?>(.*?)</td>'
                for mtFind in re.finditer( pattern ,contentHtml.content,re.S ):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        proto,rest = urllib.splittype( self.section_url_map[section_name])
                        article_url = proto + "://" + urllib.splithost( rest )[0] + "/" + mtFind.groups()[0][1:]
                        #article_url = self.section_url_map[section_name][0:-1] + mtFind.groups()[0][1:]


                    public_time = self.strip_tags(mtFind.groups()[2])

                    title = mtFind.groups()[1].decode(encoding)

                    #print public_time
                    ##print repr(title)
                    #print title
                    #print article_url
                    #sys.exit(1)

                    item = article_item(article_url, title, public_time)
                    item.set_section_name(section_name)
                    article_list.append(item)
            else:
                self.logger.error(u'没有获取到文章列表 ' + str(page_num) )
            return article_list
        except BaseException, e:
            self.logger.error(str(e))
        finally:
            return article_list



if __name__ == '__main__':
    # bj_spider = bjSpider()
    #
    # for k,v in bj_spider.section_url_map.items():
    #     bj_spider.logger.info(u'获取栏目:' + k + ":" +  bj_spider.section_folder_map[k] )
    #     for page_num in range( bj_spider.page_number ):
    #         article_list = bj_spider.stripy_article_list( k , page_num )
    #         for item in article_list:
    #             bj_spider.stripy_article_context( item )

    beijing_spider = beijingSpider()
    beijing_spider.init_log(u'北京.log')
    beijing_spider.set_save_folder_path(globalconf.save_folder['beijing'])
    beijing_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['beijing']
    beijing_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])

    for section_item in beijing_spider.section_key:
        beijing_spider.logger.info(u"获取栏目:" + section_item + ":" + beijing_spider.section_folder_map[section_item])
        for page_num in range(beijing_spider.page_number):
            article_list = beijing_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                beijing_spider.stripy_article_context(item)


