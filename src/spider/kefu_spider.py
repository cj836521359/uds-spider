# -*- coding: utf-8 -*-
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
import urllib


class kefuSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = 'http://portal.csc.sgcc.com.cn'
        # self.logger = login.initLog('xz.log')
        print 'kefuSpider'
        self.session = self.init_session()
        self.folder_base = u'客服'


        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}

        self.section_key = [
            #公司要闻
            'gsyw',
            #中心要闻
            'zxyw',
            #媒体报道
            'zytz',
            #工作动态 分成中心本部和南北分中心
            #中心本部
            'gzdt',
            #南北分中心
            'fzxdt',
            #一线风采
            'yxfc',
            #职工艺苑
            'zgyy',
        ]



        #公司要闻
        self.section_url_map[self.section_key[0]] = 'http://portal.csc.sgcc.com.cn/cscweb/zxxw/gsyw/index.shtml'
        #中心要闻
        self.section_url_map[self.section_key[1]] = 'http://portal.csc.sgcc.com.cn/cscweb/zxxw/zxyw/index.shtml'
        #媒体报道
        self.section_url_map[self.section_key[2]] = 'http://portal.csc.sgcc.com.cn/cscweb/mtbd/mtbd/index.shtml'
        #工作动态 分成中心本部和南北分中心
        #中心本部
        self.section_url_map[self.section_key[3]] = 'http://portal.csc.sgcc.com.cn/cscweb/gzdt/gzdt/index.shtml'
        #南北分中心
        self.section_url_map[self.section_key[4]] = 'http://portal.csc.sgcc.com.cn/cscweb/gzdt/fzxdt/index.shtml'
        #一线风采
        self.section_url_map[self.section_key[5]] = 'http://portal.csc.sgcc.com.cn/cscweb/yxfc/yxfc/index.shtml'
        #职工艺苑
        self.section_url_map[self.section_key[6]] = 'http://portal.csc.sgcc.com.cn/cscweb/zgyy/zgyy/index.shtml'


        #公司要闻
        self.section_folder_map[self.section_key[0]] = '公司要闻'
        #中心要闻
        self.section_folder_map[self.section_key[1]] = '中心要闻'
        #媒体报道
        self.section_folder_map[self.section_key[2]] = '媒体报道'
        #工作动态 分成中心本部和南北分中心
        #中心本部
        self.section_folder_map[self.section_key[3]] = '中心本部'
        #南北分中心
        self.section_folder_map[self.section_key[4]] = '南北分中心'
        #一线风采
        self.section_folder_map[self.section_key[5]] = '一线风采'
        #职工艺苑
        self.section_folder_map[self.section_key[6]] = '职工艺苑'


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
            #contentHtml.encoding = 'gbk'
            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<TD height=28 .+?><A href="(.*?)" target=_blank>(.*?)</A></TD>\s.*?\[(.*?)\]'
                for mtFind in re.finditer(pattern, contentHtml.text, re.S):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        article_url = '%s%s' %(self.url_base, mtFind.groups()[0])
                    title = mtFind.groups()[1]
                    public_time = mtFind.groups()[2]
                    item = article_item(article_url, title, public_time)
                    item.set_section_name(section_name)
                    article_list.append(item)

            else:
                self.logger.error(u'没有获取到文章列表 ' + str(page_num))
            return article_list
        except BaseException, e:
           self.logger.error(str(e))
        finally:
           return article_list


if __name__ == '__main__':
    kefu_spider = kefuSpider()
    kefu_spider.init_log(u'客服.log')
    kefu_spider.set_save_folder_path(globalconf.save_folder['kefu'])
    kefu_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['kefu']
    kefu_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in kefu_spider.section_key:
        kefu_spider.logger.info(u"获取栏目:" + section_item + ":" + kefu_spider.section_folder_map[section_item])
        for page_num in range(kefu_spider.page_number):
            article_list = kefu_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                kefu_spider.stripy_article_context(item)


