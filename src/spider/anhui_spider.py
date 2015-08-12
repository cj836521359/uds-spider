# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
from article_item import *

class anhuiSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = 'http://portal.ah.sgcc.com.cn'
        # self.logger = login.initLog('ah.log')
        print 'anhuiSpider'
        self.session = self.init_session()
        self.folder_base = u'安徽'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            # 公司新闻
            'gsxw',
            # 本部新闻
            'bbxw',
            # 基层动态
            'jcdt',
            # 综合资讯
            'zhzx',
            # 媒体聚焦
            'mtjj',
            ]

        # 公司新闻
        self.section_url_map[self.section_key[0]] = 'http://portal.ah.sgcc.com.cn/tbbd/index.htm'
        # 本部新闻
        self.section_url_map[self.section_key[1]] = 'http://portal.ah.sgcc.com.cn/yw/index.htm'
        # 基层动态
        self.section_url_map[self.section_key[2]] = 'http://portal.ah.sgcc.com.cn/54/index.htm'
        # 综合资讯
        self.section_url_map[self.section_key[3]] = 'http://portal.ah.sgcc.com.cn/55/index.htm'
        # 媒体聚焦
        self.section_url_map[self.section_key[4]] = 'http://portal.ah.sgcc.com.cn/mtjj/index.htm'


        # 公司新闻
        self.section_folder_map[self.section_key[0]] = u'公司新闻'
        # 本部新闻
        self.section_folder_map[self.section_key[1]] = u'本部新闻'
        # 基层动态
        self.section_folder_map[self.section_key[2]] = u'本部动态'
        # 综合资讯
        self.section_folder_map[self.section_key[3]] = u'综合资讯'
        # 媒体聚焦
        self.section_folder_map[self.section_key[4]] = u'媒体聚焦'



    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            contentHtml = None
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-4] + '_' + str(page_num) + '.htm'

            #print url
            #sys.exit(1)
            contentHtml = self.session.get(url, stream=True)
            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<td width="89%.*?<a href="(.*?)".*?>(.*?)</a></td>\s.*?span class="anav_1">(.*?)</span>'
                for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        article_url = '%s%s' %(self.section_url_map[section_name][0:-10], mtFind.groups()[0][1:])

                    public_time = mtFind.groups()[2]
                    title = mtFind.groups()[1]
                    title = title.decode()

                    item = article_item(article_url, title, public_time)
                    item.set_section_name(section_name)
                    article_list.append(item)
            else:
                self.logger.error(u'没有获取到文章列表 ' + str(page_num))
            return article_list
        except BaseException, e:
            self.logger.error(str(e))
        finally:
            return article_list


if __name__ == '__main__':
    json_dic = demjson.decode(globalconf.str)
    print len(json_dic['provinces'])
    sys.exit(1)
    anhui_spider = anhuiSpider()
    anhui_spider.init_log(u'安徽.log')
    anhui_spider.set_save_folder_path(globalconf.save_folder['anhui'])
    anhui_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['anhui']
    anhui_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in anhui_spider.section_key:
        anhui_spider.logger.info(u"获取栏目:" + section_item + ":" + anhui_spider.section_folder_map[section_item])
        for page_num in range(anhui_spider.page_number):
            article_list = anhui_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                anhui_spider.stripy_article_context(item)




