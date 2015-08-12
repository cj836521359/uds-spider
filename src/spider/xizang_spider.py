
# -*- coding: utf-8 -*-
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
import urllib

class xizangSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        print 'xizangSpider'
        self.session = self.init_session()
        self.folder_base = u'西藏'


        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}

        self.section_key = [
            # 本部动态
            'bbdt',
            # 公司新闻
            'gsxw',
            # 基层简讯
            'jcjx',
            # 行业信息
            'yhxx',
            # 媒体报道
            'mtbd',
            # 青藏联网工程_图文信息
            'qzlwgc_twxx',
            ]



        # 本部动态
        self.section_url_map[self.section_key[0]] = 'http://portal.xz.sgcc.com.cn/xz/dlxw/bbdt/index.shtml'
        # 公司新闻
        self.section_url_map[self.section_key[1]] = 'http://portal.xz.sgcc.com.cn/xz/dlxw/gsyw/index.shtml'
        # 基层简讯
        self.section_url_map[self.section_key[2]] = 'http://portal.xz.sgcc.com.cn/xz/dlxw/jcdt/index.shtml'
        # 行业信息
        self.section_url_map[self.section_key[3]] = 'http://portal.xz.sgcc.com.cn/xz/dlxw/xyxx/index.shtml'
        # 媒体报道
        self.section_url_map[self.section_key[4]] = 'http://portal.xz.sgcc.com.cn/xz/dlxw/mtbd/index.shtml'
        # 青藏联网工程_图文信息
        self.section_url_map[self.section_key[5]] = 'http://portal.xz.sgcc.com.cn/xz/dlxw/qclwgc/twxx/index.shtml'


        # 本部动态
        self.section_folder_map[self.section_key[0]] = u'本部动态'
        # 公司新闻
        self.section_folder_map[self.section_key[1]] = u'公司新闻'
        # 基层简讯
        self.section_folder_map[self.section_key[2]] = u'基层简讯'
        # 行业信息
        self.section_folder_map[self.section_key[3]] = u'行业信息'
        # 媒体报道
        self.section_folder_map[self.section_key[4]] = u'媒体报道'
        # 青藏联网工程_图文信息
        self.section_folder_map[self.section_key[5]] = u'青藏联网工程_图文信息 '


    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-6] + '_' + str(self.cur_page) + '.shtml'
            contentHtml = self.session.get(url, stream=True)
            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<a href="(.*?)" target="_self">(.*?)</a>\s.*?<span class="box_r">\[(.*?)\]</span>'
                for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        article_url = '%s%s' %(self.section_url_map[section_name][0:29], mtFind.groups()[0][1:])
                    public_time = mtFind.groups()[2]
                    title = mtFind.groups()[1]
                    title = title.decode('gbk').strip()

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
    xizang_spider = xizangSpider()
    xizang_spider.init_log(u'西藏.log')
    xizang_spider.set_save_folder_path(globalconf.save_folder['xizang'])
    xizang_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['xizang']
    xizang_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in xizang_spider.section_key:
        xizang_spider.logger.info(u"获取栏目:" + section_item + ":" + xizang_spider.section_folder_map[section_item])
        for page_num in range(xizang_spider.page_number):
            article_list = xizang_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                xizang_spider.stripy_article_context(item)








