
# -*- coding: utf-8 -*-
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
import urllib


class xinjiangSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        print 'xinjiangSpider'
        self.session = self.init_session()
        self.folder_base = u'新疆'

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
            # 媒体聚焦
            'mtjj',
            # 观点体会
            'gdth',
            # 基层动态
            'jcdt',
            # 一线传真
            'yxcz',
            # 专题报道
            'ztbd',
            # 文艺园地
            'wyyd',
            ]


        # 国网要闻
        self.section_url_map[self.section_key[0]] = 'http://portal.xj.sgcc.com.cn/site4/gsxw/gwyw/index.shtml'
        # 公司要闻
        self.section_url_map[self.section_key[1]] = 'http://portal.xj.sgcc.com.cn/site4/gsxw/gsyw/index.shtml'
        # 本部动态
        self.section_url_map[self.section_key[2]] = 'http://portal.xj.sgcc.com.cn/site4/gsxw/bbdt/index.shtml'
        # 媒体聚焦
        self.section_url_map[self.section_key[3]] = 'http://portal.xj.sgcc.com.cn/site4/gsxw/mtjj/index.shtml'
        # 观点体会
        self.section_url_map[self.section_key[4]] = 'http://portal.xj.sgcc.com.cn/site4/gsxw/gdth/index.shtml'
        # 基层动态
        self.section_url_map[self.section_key[5]] = 'http://portal.xj.sgcc.com.cn/site4/gsxw/jcdt/index.shtml'
        # 一线传真
        self.section_url_map[self.section_key[6]] = 'http://portal.xj.sgcc.com.cn/site4/gsxw/yxcz/index.shtml'
        # 专题报道
        self.section_url_map[self.section_key[7]] = 'http://portal.xj.sgcc.com.cn/site4/gsxw/ztbd/index.shtml'
        # 文艺园地
        self.section_url_map[self.section_key[8]] = 'http://portal.xj.sgcc.com.cn/site4/gsxw/wyyd/index.shtml'



        # 国网要闻
        self.section_folder_map[self.section_key[0]] = u'国网要闻'
        # 公司要闻
        self.section_folder_map[self.section_key[1]] = u'公司要闻'
        # 本部动态
        self.section_folder_map[self.section_key[2]] = u'本部动态'
        # 媒体聚焦
        self.section_folder_map[self.section_key[3]] = u'媒体聚焦'
        # 观点体会
        self.section_folder_map[self.section_key[4]] = u'观点体会'
        # 基层动态
        self.section_folder_map[self.section_key[5]] = u'基层动态'
        # 一线传真
        self.section_folder_map[self.section_key[6]] = u'一线传真'
        # 专题报道
        self.section_folder_map[self.section_key[7]] = u'专题报道'
        # 文艺园地
        self.section_folder_map[self.section_key[8]] = u'文艺园地'




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
            pattern = r'<div class=left1_list_text style=margin-top:4px><a.*?href="(.*?)".*?>(.*?)</a>.*?<div .*?\[(.*?)\]'
            for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                if mtFind.groups()[0][0:4] == "http":
                    article_url = mtFind.groups()[0]
                else:
                    proto, rest = urllib.splittype(self.section_url_map[section_name])
                    article_url = proto + "://" + urllib.splithost(rest)[0] + "/" + mtFind.groups()[0][1:]


                public_time = mtFind.groups()[2].strip('&nbsp;').strip()
                title = self.decode_data(contentHtml.encoding, mtFind.groups()[1])

                item = article_item(article_url, title, public_time)
                item.set_section_name(section_name)
                article_list.append(item)
        else:
            self.logger.error(u'没有获取到文章列表 ' + str(page_num))
        return article_list



if __name__ == '__main__':
    xinjiang_spider = xinjiangSpider()
    xinjiang_spider.init_log(u'新疆.log')
    xinjiang_spider.set_save_folder_path(globalconf.save_folder['xinjiang'])
    xinjiang_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['xinjiang']
    xinjiang_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in xinjiang_spider.section_key:
        xinjiang_spider.logger.info(u"获取栏目:" + section_item + ":" + xinjiang_spider.section_folder_map[section_item])
        for page_num in range(xinjiang_spider.page_number):
            article_list = xinjiang_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                xinjiang_spider.stripy_article_context(item)











