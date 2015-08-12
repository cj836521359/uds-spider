# -*- coding: utf-8 -*-
#import spider
from __init__ import *
from spider import *
import sys
import time
import chardet


class sichuanSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        print 'sichuanSpider'
        self.session = self.init_session()
        self.folder_base = u'四川'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}

        self.section_key = [
            #公司要闻
            'gsyw',
            #本部新闻
            'bbxw',
            #媒体报道
            'mtbd',
            #基层动态
            'jcdt',
        ]



        #公司要闻
        self.section_url_map[self.section_key[0]] = 'http://portal.sc.sgcc.com.cn/ttxw/index.shtml'
        #本部新闻
        self.section_url_map[self.section_key[1]] = 'http://portal.sc.sgcc.com.cn/bbxw/index.shtml'
        #媒体报道
        self.section_url_map[self.section_key[2]] = 'http://portal.sc.sgcc.com.cn/mtbg/index.shtml'
        #基层动态
        self.section_url_map[self.section_key[3]] = 'http://portal.sc.sgcc.com.cn/jcdt/index.shtml'


        #公司要闻
        self.section_folder_map[self.section_key[0]] = u'公司要闻'
        #本部新闻
        self.section_folder_map[self.section_key[1]] = u'本部新闻'
        #媒体报道
        self.section_folder_map[self.section_key[2]] = u'媒体报道'
        #基层动态
        self.section_folder_map[self.section_key[3]] = u'基层动态'

        # self.init_mkdir_folder()


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
                pattern = r'<div class=left1_list_text style=margin-top:4px><a class=lg href="(.*?)">(.*?)</a>.*?\[(.*?)\].*?</li>'
                for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        article_url = '%s%s' %(self.section_url_map[section_name][0:-16], mtFind.groups()[0][1:])

                    public_time = mtFind.groups()[2]

                    title = mtFind.groups()[1]
                    title = title.decode(encoding).strip()

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
    sichuan_spider = sichuanSpider()
    sichuan_spider.init_log(u'四川.log')
    sichuan_spider.set_save_folder_path(globalconf.save_folder['sichuan'])
    sichuan_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['sichuan']
    sichuan_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in sichuan_spider.section_key:
        sichuan_spider.logger.info(u"获取栏目:" + section_item + ":" + sichuan_spider.section_folder_map[section_item])
        for page_num in range(sichuan_spider.page_number):
            article_list = sichuan_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                sichuan_spider.stripy_article_context(item)






