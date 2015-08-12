# -*- coding: utf-8 -*-
#import spider
from spider import *
import sys
import time
import chardet
import urllib

class jilinSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = 'http://portal.jl.sgcc.com.cn'
        print 'jilinSpider'
        self.session = self.init_session()
        self.folder_base = u'吉林'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            #国网要闻
            'gwxw',
            #公司要闻
            'gsyw',
            #本部动态
            'bbxw',
            #媒体反应
            'mtfy',
            #基层动态
            'jcdt',
            #最新通知
            'zytz',
            ]

        # 国网要闻
        self.section_url_map[self.section_key[0]] = 'http://portal.jl.sgcc.com.cn/jl/gwxw/index.shtml'
        # 公司要闻
        self.section_url_map[self.section_key[1]] = 'http://portal.jl.sgcc.com.cn/jl/gsyw/index.shtml'
        # 本部动态
        self.section_url_map[self.section_key[2]] = 'http://portal.jl.sgcc.com.cn/jl/bbxw/index.shtml'
        # 媒体反应
        self.section_url_map[self.section_key[3]] = 'http://portal.jl.sgcc.com.cn/jl/mtfy/index.shtml'
        # 基层动态
        self.section_url_map[self.section_key[4]] = 'http://portal.jl.sgcc.com.cn/jl/jcdt/index.shtml'
         #最新通知
        self.section_url_map[self.section_key[5]] = 'http://portal.jl.sgcc.com.cn/jl/zytz/index.shtml'

        # 国网要闻
        self.section_folder_map[self.section_key[0]] = u'国网要闻'
        # 公司要闻
        self.section_folder_map[self.section_key[1]] = u'公司要闻'
        # 本部动态
        self.section_folder_map[self.section_key[2]] = u'本部动态'
        # 媒体反应
        self.section_folder_map[self.section_key[3]] = u'媒体反应'
        # 基层动态
        self.section_folder_map[self.section_key[4]] = u'基层动态'
        # 最新通知
        self.section_folder_map[self.section_key[5]] = u'最新通知'



        #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-6] + '_' + str(page_num) + '.shtml'
            contentHtml = self.session.get(url)
            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<a class=lg href="(.*?)">(.*?)</a>.*?\[(.*?)\]'
                for mtFind in re.finditer(pattern, contentHtml.text):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        article_url = '%s%s' %(self.url_base, mtFind.groups()[0])
                    title = mtFind.groups()[1]
                    public_time = mtFind.groups()[2]
                    item = article_item(article_url, title, public_time)
                    item.set_section_name(section_name)
                    article_list.append(item)
        except BaseException, e:
            self.logger.error(str(e))
        finally:
            return article_list







if __name__ == '__main__':
    jilin_spide = jilinSpider()
    jilin_spide.init_log(u'吉林.log')
    jilin_spide.set_save_folder_path(globalconf.save_folder['jilin'])
    jilin_spide.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['jilin']
    jilin_spide.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in jilin_spide.section_key:
        jilin_spide.logger.info(u"获取栏目:" + section_item + ":" + jilin_spide.section_folder_map[section_item])
        for page_num in range(jilin_spide.page_number):
            article_list = jilin_spide.stripy_article_list(section_item, page_num)
            for item in article_list:
                jilin_spide.stripy_article_context(item)
