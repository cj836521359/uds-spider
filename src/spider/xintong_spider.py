# -*- coding: utf-8 -*-
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
import urllib


class xintongSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = 'http://portalnew.sgit.sgcc.com.cn'
        print 'xintongSpider'
        self.session = self.init_session()
        self.folder_base = u'信通'


        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            #公司要闻
            'gsyw',
            #总部动态
            'zbdt',
            #行业动态
            'xydt',
            #关注与视野
            'gzysy',
            #信通交流
            'xtjl',
        ]

        # 公司要闻
        self.section_url_map[self.section_key[0]] = 'http://portalnew.sgit.sgcc.com.cn/xtxb2013/gsyw/index.shtml'
        # 总部动态
        self.section_url_map[self.section_key[1]] = 'http://portalnew.sgit.sgcc.com.cn/xtxb2013/zbdt/index.shtml'
        # 行业动态
        self.section_url_map[self.section_key[2]] = 'http://portalnew.sgit.sgcc.com.cn/xtxb2013/xydt/index.shtml'
        # 关注与视野
        self.section_url_map[self.section_key[3]] = 'http://portalnew.sgit.sgcc.com.cn/xtxb2013/gzysy/index.shtml'
        # 信通交流
        self.section_url_map[self.section_key[4]] = 'http://portalnew.sgit.sgcc.com.cn/xtxb2013/xtjl/index.shtml'


        # 公司要闻
        self.section_folder_map[self.section_key[0]] = '公司要闻'
        # 总部动态
        self.section_folder_map[self.section_key[1]] = '总部动态'
        # 行业动态
        self.section_folder_map[self.section_key[2]] = '行业动态'
        # 关注与视野
        self.section_folder_map[self.section_key[3]] = '关注与视野'
        # 信通交流
        self.section_folder_map[self.section_key[4]] = '信通交流'



    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-6] + '_' + str(page_num) + '.shtml'
            self.logger.info(url)

            contentHtml = self.session.get(url)
            encoding = chardet.detect(contentHtml.content)['encoding']

            if contentHtml.encoding == 'ISO-8859-1':
                contentHtml.encoding = 'gbk'
            else:
                contentHtml.encoding = 'utf-8'

            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<li><a target.*? href="(.*?)">(.*?)</a>.*?\[(.*?)\]'
                for mtFind in re.finditer(pattern, contentHtml.text):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        article_url = '%s%s' %(self.url_base, mtFind.groups()[0])
                        title = mtFind.groups()[1]
                        public_time = mtFind.groups()[2].strip()

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
    xintong_spider = xintongSpider()
    xintong_spider.init_log(u'信通.log')
    xintong_spider.set_save_folder_path(globalconf.save_folder['xintong'])
    xintong_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['xintong']
    xintong_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in xintong_spider.section_key:
        xintong_spider.logger.info(u"获取栏目:" + section_item + ":" + xintong_spider.section_folder_map[section_item])
        for page_num in range(xintong_spider.page_number):
            article_list = xintong_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                xintong_spider.stripy_article_context(item)



