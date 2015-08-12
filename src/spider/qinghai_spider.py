
# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
import urllib

class qinghaiSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        # self.logger = login.initLog('qh.log')
        print 'qinghaiSpider'
        self.session = self.init_session()
        self.folder_base = u'青海'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            #头条新闻
            'ttxw',
            #青电快讯
            'qdkx',
            #媒体聚焦
            'mtjj',
            #图片新闻
            'tpxw',
            #公告
            'gg',
        ]

        # 头条新闻
        self.section_url_map[self.section_key[0]] = 'http://portal.qh.sgcc.com.cn/ttxw/index.shtml'
        # 青电快讯
        self.section_url_map[self.section_key[1]] = 'http://portal.qh.sgcc.com.cn/qdkx/index.shtml'
        # 媒体聚焦
        self.section_url_map[self.section_key[2]] = 'http://portal.qh.sgcc.com.cn/mtjj/index.shtml'
        # 图片新闻
        self.section_url_map[self.section_key[3]] = 'http://portal.qh.sgcc.com.cn/tpxw/index.shtml'
        # 公告
        self.section_url_map[self.section_key[4]] = 'http://portal.qh.sgcc.com.cn/gg/index.shtml'


        # 头条新闻
        self.section_folder_map[self.section_key[0]] = u'头条新闻'
        # 青电快讯
        self.section_folder_map[self.section_key[1]] = u'青电快讯'
        # 媒体聚焦
        self.section_folder_map[self.section_key[2]] = u'媒体聚焦'
        # 图片新闻
        self.section_folder_map[self.section_key[3]] = u'图片新闻'
        # 公告
        self.section_folder_map[self.section_key[4]] = u'公告'



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
            encoding = chardet.detect(contentHtml.content)['encoding']
            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<span class="box_r">\[(.*?)\]</span>.*?<a href="(.*?)".*?>(.*?)</a>'
                for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                    if mtFind.groups()[1][0:4] == "http":
                        article_url = mtFind.groups()[1]
                    else:
                        proto, rest = urllib.splittype(self.section_url_map[section_name])
                        article_url = proto + "://" + urllib.splithost(rest)[0] + "/" + mtFind.groups()[1][1:]

                    public_time = mtFind.groups()[0].strip('&nbsp;').strip()
                    print public_time
                    title = mtFind.groups()[2].decode(encoding).strip()
                    title = self.strip_tags(title)
                    print title
                    print article_url

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
    qinghai_spider = qinghaiSpider()
    qinghai_spider.init_log(u'青海.log')
    qinghai_spider.set_save_folder_path(globalconf.save_folder['qinghai'])
    qinghai_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['qinghai']
    qinghai_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in qinghai_spider.section_key:
        qinghai_spider.logger.info(u"获取栏目:" + section_item + ":" + qinghai_spider.section_folder_map[section_item])
        for page_num in range(qinghai_spider.page_number):
            article_list = qinghai_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                qinghai_spider.stripy_article_context(item)










