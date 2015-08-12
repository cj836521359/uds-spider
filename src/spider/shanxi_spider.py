# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
import urllib

class shanxiSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        print 'shanxiSpider'
        self.session = self.init_session()
        self.folder_base = u'山西'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            # 公司要闻
            'gsyw',
            # 基层动态
            'jcdt',
            # 媒体报道
            'mtbd',
            # 图片新闻
            'tpxw',
            # 本部要闻
            'bbyw',
            # 一线风采
            'yxfc',
        ]


        self.section_url_map[self.section_key[0]] = 'http://system.sx.sgcc.com.cn/channels/c3728_1.html'
        self.section_url_map[self.section_key[1]] = 'http://system.sx.sgcc.com.cn/channels/c3729_1.html'
        self.section_url_map[self.section_key[2]] = 'http://system.sx.sgcc.com.cn/channels/c3730_1.html'
        self.section_url_map[self.section_key[3]] = 'http://system.sx.sgcc.com.cn/channels/c3726_1.html'
        self.section_url_map[self.section_key[4]] = 'http://system.sx.sgcc.com.cn/channels/c6627_1.html'
        self.section_url_map[self.section_key[5]] = 'http://system.sx.sgcc.com.cn/channels/c10912_1.html'


        # 公司要闻
        self.section_folder_map[self.section_key[0]] = u'公司要闻'
        # 基层动态
        self.section_folder_map[self.section_key[1]] = u'基层动态'
        # 媒体报道
        self.section_folder_map[self.section_key[2]] = u'媒体报道'
        # 图片新闻
        self.section_folder_map[self.section_key[3]] = u'图片新闻'
        # 本部要闻
        self.section_folder_map[self.section_key[4]] = u'本部要闻'
        # 一线风采
        self.section_folder_map[self.section_key[5]] = u'一线风采'



    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            contentHtml = None
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-6] +  str(self.cur_page) + '.html'


            contentHtml = self.session.get(url, stream=True)
            encoding = chardet.detect(contentHtml.content)['encoding']

            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<a  onclick="window.open.*?href=\'(.*?)\'\s*>(.*?)</a></td>.*?>(.*?)</td>'
                for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        proto,rest = urllib.splittype(self.section_url_map[section_name])
                        article_url = proto + "://" + urllib.splithost( rest )[0] + "/" + mtFind.groups()[0][1:]

                    public_time = self.strip_tags(mtFind.groups()[2])
                    title = mtFind.groups()[1].decode(encoding)

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
    shanxi_spider = shanxiSpider()
    shanxi_spider.init_log(u'山西.log')
    shanxi_spider.set_save_folder_path(globalconf.save_folder['shanxi'])
    shanxi_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['shanxi']
    shanxi_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in shanxi_spider.section_key:
        shanxi_spider.logger.info(u"获取栏目:" + section_item + ":" + shanxi_spider.section_folder_map[section_item])
        for page_num in range(shanxi_spider.page_number):
            article_list = shanxi_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                shanxi_spider.stripy_article_context(item)
