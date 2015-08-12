# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'
from spider import *
import sys
import time
import chardet
from src.spider.article_item import article_item

class chongqingSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        print 'chongqingSpide'
        self.session = self.init_session()
        self.folder_base = u'重庆'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}

        self.section_key = [
        # 公司要闻
        'gsyw',
        # 国网要闻
        'gwyw',
        # 基层动态
        'jcdt',
        # 群众性科技创新
        'czxkjcx',
        ]





        #公司要闻
        self.section_url_map[self.section_key[0]] = 'http://system.cq.sgcc.com.cn/cqsgcc/gsxw/dlyw/list_42_1.html'
        #国网要闻
        self.section_url_map[self.section_key[1]] = 'http://system.cq.sgcc.com.cn/cqsgcc/gsxw/guowangyaowen/list_229_1.html'
        #基层动态
        self.section_url_map[self.section_key[2]] = 'http://system.cq.sgcc.com.cn/cqsgcc/gsxw/jcdt/list_50_1.html'
        #群众性科技创新
        self.section_url_map[self.section_key[3]] = 'http://system.cq.sgcc.com.cn/cqsgcc/gsxw/jcdt/qunzhongxingkejichuangxin/list_247_1.html'



        # 公司要闻
        self.section_folder_map[self.section_key[0]] = u'公司要闻'
        # 国网要闻
        self.section_folder_map[self.section_key[1]] = u'国网要闻'
        # 基层动态
        self.section_folder_map[self.section_key[2]] = u'基层动态'
        # 群众性科技创新
        self.section_folder_map[self.section_key[3]] = u'群众性科技创新'

        # self.init_mkdir_folder()


    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        self.cur_page = page_num
        article_list = []
        if page_num == 0:
            url = self.section_url_map[section_name]
        else:
            url = self.section_url_map[section_name][0:-7] + '_' + str(self.cur_page) + '.html'
        #print url
        #sys.exit(1)

        contentHtml = self.session.get(url, stream=True)
        #common_utils.write_to_file_with_stream(contentHtml.content,'cqqqqq.txt')
        #sys.exit(1)

        if contentHtml.status_code == requests.codes.ok:
            pattern = r'[^>]<a href="(.*?)" class="title" target="_blank">(.*?)</a>\s.*?<span\s.*?\[(.*?)\]'
            for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                if mtFind.groups()[0][0:4] == "http":
                    article_url = mtFind.groups()[0]
                else:
                    article_url = '%s%s' %(self.section_url_map[section_name][0:29], mtFind.groups()[0][1:])


                #print article_url
                #sys.exit()

                #public_time = mtFind.groups()[2]
                #public_time = time.strptime(mtFind.groups()[2],"%Y-%m-%d")
                public_time = mtFind.groups()[2]

                title = mtFind.groups()[1]
                title = title.decode('gbk').strip()
                title = self.strip_tags(title)
                #print title
                ##print article_url
                #sys.exit(1)

                item = article_item(article_url, title, public_time )
                item.set_section_name(section_name)
                # if time.strptime(public_time, '%Y-%m-%d' ).tm_year == 2015:
                article_list.append(item)
        else:
            self.logger.error(u'没有获取到文章列表 ' + str(page_num) )
        return article_list


if __name__ == '__main__':
    # cq_spider = chongqingSpide()
    #
    # for k,v in cq_spider.section_url_map.items():
    #     cq_spider.logger.info(u'获取栏目:' + k + ":" +  cq_spider.section_folder_map[k] )
    #     for page_num in range( cq_spider.page_number ):
    #         article_list = cq_spider.stripy_article_list( k , page_num )
    #         for item in article_list:
    #             cq_spider.stripy_article_context( item )

    chongqing_spider = chongqingSpider()
    chongqing_spider.init_log(u'重庆.log')
    chongqing_spider.set_save_folder_path(globalconf.save_folder['chongqing'])
    chongqing_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['chongqing']
    chongqing_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in chongqing_spider.section_key:
        chongqing_spider.logger.info(u"获取栏目:" + section_item + ":" + chongqing_spider.section_folder_map[section_item])
        for page_num in range(chongqing_spider.page_number):
            article_list = chongqing_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                chongqing_spider.stripy_article_context(item)





