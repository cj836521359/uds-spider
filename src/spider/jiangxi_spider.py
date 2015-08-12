# -*- coding: utf-8 -*-
#import spider
from spider import *
import sys
import time
import chardet
import urllib

class jiangxiSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        # self.logger = login.initLog('jx.log')
        print 'jiangxiSpider'
        self.session = self.init_session()
        self.folder_base = u'江西'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            # 国网要闻
            'gwxw',
            # 公司要闻
            'gsyw',
            # 本部新闻
            'bbxw',
            # 基层动态
            'jcdt',
            # 媒体报道
            'mtbd',
            # 领导讲话
            'ldjh',
            ]


        #国网要闻
        self.section_url_map[self.section_key[0]] = 'http://porta1.jx.sgcc.com.cn/main/subject/191707/ArticleList191707_1.shtml'
        #公司要闻
        self.section_url_map[self.section_key[1]] = 'http://porta1.jx.sgcc.com.cn/main/subject/8/ArticleList8_1.shtml'
        #本部新闻
        self.section_url_map[self.section_key[2]] = 'http://porta1.jx.sgcc.com.cn/main/subject/112480/ArticleList112480_1.shtml'
        #基层动态
        self.section_url_map[self.section_key[3]] = 'http://porta1.jx.sgcc.com.cn/main/subject/1082/ArticleList1082_1.shtml'
        #媒体报道
        self.section_url_map[self.section_key[4]] = 'http://porta1.jx.sgcc.com.cn/main/subject/93076/ArticleList93076_1.shtml'
        #领导讲话
        self.section_url_map[self.section_key[5]] = 'http://porta1.jx.sgcc.com.cn/main/subject/93080/ArticleList93080_1.shtml'


        #国网要闻
        self.section_folder_map[self.section_key[0]] = u'国网要闻'
        #公司要闻
        self.section_folder_map[self.section_key[1]] = u'公司要闻'
        #本部新闻
        self.section_folder_map[self.section_key[2]] = u'本部新闻'
        #基层动态
        self.section_folder_map[self.section_key[3]] = u'基层动态'
        #媒体报道
        self.section_folder_map[self.section_key[4]] = u'媒体报道'
        #领导讲话
        self.section_folder_map[self.section_key[5]] = u'领导讲话'




    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-8] + '_' + str(self.cur_page) + '.shtml'

            contentHtml = self.session.get(url, stream=True)
            encoding = chardet.detect(contentHtml.content)['encoding']

            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<a href=\'(.*?)\'.*?<font class=a19_articlelist>(.*?)</a>.*?>(.*?)</td>'
                for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        proto,rest = urllib.splittype( self.section_url_map[section_name])
                        article_url = proto + "://" + urllib.splithost( rest )[0] + "/" + mtFind.groups()[0].strip("../")


                    public_time = self.strip_tags(mtFind.groups()[2])
                    title = mtFind.groups()[1].decode(encoding)

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
    jiangxi_spider.init_log(u'江西.log')
    jiangxi_spider.set_save_folder_path(globalconf.save_folder['jiangxi'])
    jiangxi_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['jiangxi']
    jiangxi_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in jiangxi_spider.section_key:
        jiangxi_spider.logger.info(u"获取栏目:" + section_item + ":" + jiangxi_spider.section_folder_map[section_item])
        for page_num in range(jiangxi_spider.page_number):
            article_list = jiangxi_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                jiangxi_spider.stripy_article_context(item)
















