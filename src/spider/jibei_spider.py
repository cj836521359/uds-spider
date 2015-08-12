# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet


class jibeiSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = 'http://www.jibei.sgcc.com.cn'
        print 'jibeiSpider'
        self.session = self.init_session()
        self.folder_base = u'冀北'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            # 公司要闻
            'gsyw',
            # 本部新闻
            'bbxw',
            # 基层动态-地市公司
            'jcdt_dsgs',
            # 基层动态-县供电公司
            'jcdt_sgdgs',
            # 冀北时评
            'jbsp',
            # 热点专题
            'rdzt',
        ]


        self.section_url_map[self.section_key[0]] = 'http://www.jibei.sgcc.com.cn/gsxw/gsyw/index.shtml'
        self.section_url_map[self.section_key[1]] = 'http://www.jibei.sgcc.com.cn/gskx/index.shtml'
        self.section_url_map[self.section_key[2]] = 'http://www.jibei.sgcc.com.cn/jcdtlm/gdzhdwdt/index.shtml'
        self.section_url_map[self.section_key[3]] = 'http://www.jibei.sgcc.com.cn/jcdtlm/xgdgsdt/index.shtml'
        self.section_url_map[self.section_key[4]] = 'http://www.jibei.sgcc.com.cn/jbsp/index.shtml'
        self.section_url_map[self.section_key[5]] = 'http://www.jibei.sgcc.com.cn/rdzt/index.shtml'


        # 公司要闻
        self.section_folder_map[self.section_key[0]] = u'公司要闻'
        # 本部新闻
        self.section_folder_map[self.section_key[1]] = u'本部新闻'
        # 基层动态-地市公司
        self.section_folder_map[self.section_key[2]] = u'基层动态-地市公司'
        # 基层动态-县供电公司
        self.section_folder_map[self.section_key[3]] = u'基层动态-县供电公司'
        # 冀北时评
        self.section_folder_map[self.section_key[4]] = u'冀北时评'
        # 热点专题
        self.section_folder_map[self.section_key[5]] = u'热点专题'


    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        self.cur_page = page_num
        article_list = []
        contentHtml = None
        if page_num == 0:
            url = self.section_url_map[section_name]
        else:
            url = self.section_url_map[section_name][0:-6] + '_' + str(page_num) + '.shtml'
        contentHtml = self.session.get(url, stream=True)

        if contentHtml.status_code == requests.codes.ok:
            pattern = r'<div class=\'zskz1\'><a href=\'(.*?)\'.*?>(.*?)</a></div></div><div class=\'time1\'>\[(.*?)\]</div>'
            for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                if mtFind.groups()[0][0:4] == "http":
                    article_url = mtFind.groups()[0]
                else:
                    article_url = '%s%s' %(self.url_base, mtFind.groups()[0])

                public_time = mtFind.groups()[2]
                title = mtFind.groups()[1]
                title = title.decode("gbk")
                item = article_item(article_url, title, public_time)
                item.set_section_name(section_name)
                article_list.append(item)
        else:
            self.logger.error(u'没有获取到文章列表 ' + str(page_num) )
        return article_list


if __name__ == '__main__':

    jibei_spider = jibeiSpider()
    jibei_spider.init_log(u'冀北.log')
    jibei_spider.set_save_folder_path(globalconf.save_folder['jibei'])
    jibei_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['jibei']
    jibei_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in jibei_spider.section_key:
        jibei_spider.logger.info(u"获取栏目:" + section_item + ":" + jibei_spider.section_folder_map[section_item])
        for page_num in range(jibei_spider.page_number):
            article_list = jibei_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                jibei_spider.stripy_article_context(item)

