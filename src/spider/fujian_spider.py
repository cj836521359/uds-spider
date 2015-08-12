# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet

class fujianSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = 'http://portal.ah.sgcc.com.cn'
        print 'fujianSpider'
        self.session = self.init_session()
        self.folder_base = u'福建'

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
            # 本部新闻
            'bbxw',
            # 媒体报道
            'mtbd',
            # 最新通知
            'zxtz',
            ]


        # 国网要闻
        self.section_url_map[self.section_key[0]] = 'http://portal.fj.sgcc.com.cn/3/715/mrows20/frow0/channelIndex.htm'
        # 公司要闻
        self.section_url_map[self.section_key[1]] = 'http://portal.fj.sgcc.com.cn/3/8/mrows20/frow0/channelIndex.htm'
        # 本部新闻
        self.section_url_map[self.section_key[2]] = 'http://portal.fj.sgcc.com.cn/3/757/mrows20/frow0/channelIndex.htm'
        # 媒体报道
        self.section_url_map[self.section_key[3]] = 'http://portal.fj.sgcc.com.cn/3/9/mrows20/frow0/channelIndex.htm'
        # 最新通知
        self.section_url_map[self.section_key[4]] = 'http://portal.fj.sgcc.com.cn/3/10/mrows20/frow0/channelIndex.htm'


        # 国网要闻
        self.section_folder_map[self.section_key[0]] = u'国网要闻'
        # 公司要闻
        self.section_folder_map[self.section_key[1]] = u'公司要闻'
        # 本部新闻
        self.section_folder_map[self.section_key[2]] = u'本部新闻'
        # 媒体报道
        self.section_folder_map[self.section_key[3]] = u'媒体报道'
        # 最新通知
        self.section_folder_map[self.section_key[4]] = u'最新通知'



    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            contentHtml = None
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-18] + str(page_num*20) + '/channelIndex.htm'
            contentHtml = self.session.get(url, stream=True)
            encoding = chardet.detect(contentHtml.content)['encoding']

            #logger.info(u'获取文章列表' + self.section_folder_map[section_name])
            self.logger.info(u'获取文章列表:' + self.section_folder_map[section_name] + "_" + str(self.cur_page))
            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<a class="lg12" .*? href="(.*?)"\s.*?<font color="#333333">\s(.*?)</font>\s.*?<td width="10%"  class="g12">\[(.*?)\]</td>'
                for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        article_url = '%s%s' %(self.section_url_map[section_name][0:-10], mtFind.groups()[0][1:])

                    public_time = "20" + mtFind.groups()[2]
                    public_time = time.strftime("%Y-%m-%d", time.strptime(public_time, "%Y/%m/%d"))
                    title = mtFind.groups()[1]
                    title = title.decode(encoding).strip()

                    item = article_item(article_url, title, public_time)
                    item.set_section_name(section_name)
                    # if time.strptime(public_time, '%Y-%m-%d').tm_year == 2015:
                    article_list.append(item)
            else:
                self.logger.error(u'没有获取到文章列表 ' + str(page_num))
            return article_list
        except BaseException, e:
            self.logger.error(str(e))
        finally:
            return article_list

if __name__ == '__main__':
    fujian_spider = fujianSpider()
    fujian_spider.init_log(u'福建.log')
    fujian_spider.set_save_folder_path(globalconf.save_folder['fujian'])
    fujian_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['fujian']
    fujian_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in fujian_spider.section_key:
        fujian_spider.logger.info(u"获取栏目:" + section_item + ":" + fujian_spider.section_folder_map[section_item])
        for page_num in range(fujian_spider.page_number):
            article_list = fujian_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                fujian_spider.stripy_article_context(item)





