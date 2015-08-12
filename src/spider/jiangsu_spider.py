# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'

from __init__ import *
from spider import *
import sys
import time
import chardet


class jiangsuSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = 'http://system.js.sgcc.com.cn'
        # self.logger = login.initLog('jb.log')
        print 'jiangsuSpider'
        self.session = self.init_session()
        self.folder_base = u'江苏'

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
            # 本部动态
            'bbdt',
            # 媒体报道
            'mtbd',
            # 广角镜
            'jbsp',
            # 基层链接市
            'jcljs',
            # 基层链接县
            'jcljx',
        ]


        self.section_url_map[self.section_key[0]] = 'http://system.js.sgcc.com.cn/col/col5332/index.html'
        self.section_url_map[self.section_key[1]] = 'http://system.js.sgcc.com.cn/col/col957/index.html'
        self.section_url_map[self.section_key[2]] = 'http://system.js.sgcc.com.cn/col/col4113/index.html'
        self.section_url_map[self.section_key[3]] = 'http://system.js.sgcc.com.cn/col/col963/index.html'
        self.section_url_map[self.section_key[4]] = 'http://system.js.sgcc.com.cn/col/col1028/index.html'
        self.section_url_map[self.section_key[5]] = 'http://system.js.sgcc.com.cn/col/col959/index.html'
        self.section_url_map[self.section_key[6]] = 'http://system.js.sgcc.com.cn/col/col961/index.html'


        # 国网要闻
        self.section_folder_map[self.section_key[0]] = u'国网要闻'
        # 公司要闻
        self.section_folder_map[self.section_key[1]] = u'公司要闻'
        # 本部动态
        self.section_folder_map[self.section_key[2]] = u'本部动态'
        # 媒体报道
        self.section_folder_map[self.section_key[3]] = u'媒体报道'
        # 广角镜
        self.section_folder_map[self.section_key[4]] = u'广角镜'
        # 基层链接市
        self.section_folder_map[self.section_key[5]] = u'基层链接市'
        # 基层链接县
        self.section_folder_map[self.section_key[6]] = u'基层链接县'




    # 爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            contentHtml = None
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-6] + '_' + str(page_num) + '.shtml'
            contentHtml = self.session.get(url, stream=True)
            if contentHtml.status_code == requests.codes.ok:
                pattern = r'urls\[i\]=\'(.*?)\';headers\[i\]=\'(.*?)\';year\[i\]=\'(.*?)\';month\[i\]=\'(.*?)\';day\[i\]=\'(.*?)\''
                for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        article_url = '%s%s' %(self.url_base, mtFind.groups()[0])

                    public_time = mtFind.groups()[2] + "-" + mtFind.groups()[3] + "-" + mtFind.groups()[4]
                    title = mtFind.groups()[1]
                    title = title.decode()

                    item = article_item(article_url, title, public_time)
                    item.set_section_name(section_name)
                    article_list.append(item)
            else:
                self.logger.error(u'没有获取到文章列表 ' + str(page_num) )
        except BaseException, e:
            self.logger.error(str(e))
        finally:
            return article_list


if __name__ == '__main__':
    jiangsu_spider = jiangsuSpider()
    jiangsu_spider.init_log(u'江苏.log')
    jiangsu_spider.set_save_folder_path(globalconf.save_folder['jiangsu'])
    jiangsu_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['jiangsu']
    jiangsu_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in jiangsu_spider.section_key:
        jiangsu_spider.logger.info(u"获取栏目:" + section_item + ":" + jiangsu_spider.section_folder_map[section_item])
        for page_num in range(jiangsu_spider.page_number):
            article_list = jiangsu_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                jiangsu_spider.stripy_article_context(item)


