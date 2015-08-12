
# -*- coding: utf-8 -*-
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
import urllib


class ningxiaSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        # self.logger = login.initLog('nx.log')
        print 'ningxiaSpider'
        self.session = self.init_session()
        self.folder_base = u'宁夏'
            # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
                #国网要闻
                'gwyw',
                #公司新闻
                'gsxw',
                #通讯报道
                'txbd',
                #媒体报道
                'mtbd',
                #行业新闻
                'xyxw_gwdt',
                #综合信息
                'zxxx',
                #基层动态
                'jcdt',
                ]


        #国网要闻
        self.section_url_map[self.section_key[0]] = 'http://portal.nx.sgcc.com.cn/WEB/gwyw/index.shtml'
        #公司新闻
        self.section_url_map[self.section_key[1]] = 'http://portal.nx.sgcc.com.cn/WEB/gsxws/gsxw/index.shtml'
        #通讯报道
        self.section_url_map[self.section_key[2]] = 'http://portal.nx.sgcc.com.cn/WEB/gsxws/txbd/index.shtml'
        #媒体报道
        self.section_url_map[self.section_key[3]] = 'http://portal.nx.sgcc.com.cn/WEB/gsxws/mtjj/index.shtml'
        #行业新闻
        self.section_url_map[self.section_key[4]] = 'http://portal.nx.sgcc.com.cn/WEB/gsxws/xyxw/gwdt/index.shtml'
        #综合信息
        self.section_url_map[self.section_key[5]] = 'http://portal.nx.sgcc.com.cn/WEB/gsxws/xyxw/zhxx/index.shtml'
        #基层动态
        self.section_url_map[self.section_key[6]] = 'http://portal.nx.sgcc.com.cn/WEB/jcdt/jcdt/index.shtml'


        #国网要闻
        self.section_folder_map[self.section_key[0]] = u'国网要闻 '
        #公司新闻
        self.section_folder_map[self.section_key[1]] = u'公司新闻'
        #通讯报道
        self.section_folder_map[self.section_key[2]] = u'通讯报道'
        #媒体报道
        self.section_folder_map[self.section_key[3]] = u'媒体报道'
        #行业新闻
        self.section_folder_map[self.section_key[4]] = u'行业新闻'
        #综合信息
        self.section_folder_map[self.section_key[5]] = u'综合信息'
        #基层动态
        self.section_folder_map[self.section_key[6]] = u'基层动态'




    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        self.cur_page = page_num
        article_list = []
        if page_num == 0:
            url = self.section_url_map[section_name]
        else:
            url = self.section_url_map[section_name][0:-6] + '_' + str(self.cur_page) + '.shtml'

        contentHtml = self.session.get(url, stream=True)
        if contentHtml.status_code == requests.codes.ok:
            pattern = r'<a class=lg href="(.*?)".*?>(.*?)</a>.*?\[(.*?)\]'
            for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                if mtFind.groups()[0][0:4] == "http":
                    article_url = mtFind.groups()[0]
                else:
                    proto, rest = urllib.splittype(self.section_url_map[section_name])
                    article_url = proto + "://" + urllib.splithost(rest)[0] + "/" + mtFind.groups()[0][1:]


                public_time = mtFind.groups()[2].strip('&nbsp;').strip()
                if contentHtml.encoding == 'UTF-8':
                    title = mtFind.groups()[1].decode('UTF-8').strip()
                elif contentHtml.encoding == "GBK" or contentHtml.encoding == None:
                    title = mtFind.groups()[1].decode('gbk').strip()
                else:
                    title = mtFind.groups()[1]
                title = self.strip_tags(title)
                #print repr(title)

                item = article_item(article_url, title, public_time)
                item.set_section_name(section_name)
                article_list.append(item)
        else:
            self.logger.error(u'没有获取到文章列表 ' + str(page_num))
        return article_list



if __name__ == '__main__':
    ningxia_spider = ningxiaSpider()
    ningxia_spider.init_log(u'宁夏.log')
    ningxia_spider.set_save_folder_path(globalconf.save_folder['ningxia'])
    ningxia_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['ningxia']
    ningxia_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in ningxia_spider.section_key:
        ningxia_spider.logger.info(u"获取栏目:" + section_item + ":" + ningxia_spider.section_folder_map[section_item])
        for page_num in range(ningxia_spider.page_number):
            article_list = ningxia_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                ningxia_spider.stripy_article_context(item)











