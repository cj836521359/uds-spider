# -*- coding: utf-8 -*-
__author__ = 'chencharles'
#import spider
from spider import *
import sys
import time
import chardet
import urllib

class liaoningSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        # self.logger = login.initLog('ln.log')
        print 'liaoningSpider'
        self.session = self.init_session()
        self.folder_base = u'辽宁'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            #公司要闻
            'gsyw',
            #基层动态
            'jcdt',
            #会议通知
            'hytz',
            #本部新闻
            'bbxw',
            #企业信息
            'qyxx',
            ]


        #公司要闻
        self.section_url_map[self.section_key[0]] = 'http://www.ln.sgcc.com.cn/EipWeb/portlets/xxfb/pageflow/showArticle/showAll.do?end=&nowPage=0&start=&channelId=0000000500117d42bf9de&title=&departname=&doAction=next'
        #基层动态
        self.section_url_map[self.section_key[1]] = 'http://www.ln.sgcc.com.cn/EipWeb/portlets/xxfb/pageflow/showArticle/showAll.do?end=&nowPage=0&start=&channelId=0000000300117d42bf9de&title=&departname=&doAction=next'
        #会议通知
        self.section_url_map[self.section_key[2]] = 'http://www.ln.sgcc.com.cn/EipWeb/portlets/xxfb/pageflow/showArticle/showAll.do?end=&nowPage=0&start=&channelId=06D54245E8CABF39DBCCBDFE38FE731D&title=&departname=&doAction=next'
        #本部新闻
        self.section_url_map[self.section_key[3]] = 'http://www.ln.sgcc.com.cn/EipWeb/portlets/xxfb/pageflow/showArticle/showAll.do?end=&nowPage=0&start=&channelId=000000010011d61d6782&title=&departname=&doAction=next'
        #企业信息
        self.section_url_map[self.section_key[4]] = 'http://www.ln.sgcc.com.cn/EipWeb/portlets/xxfb/pageflow/showArticle/showAll.do?end=&nowPage=0&start=&channelId=00000001100117d42bf9de&title=&departname=&doAction=next'


        #公司要闻
        self.section_folder_map[self.section_key[0]] =u'公司要闻'
        #基层动态
        self.section_folder_map[self.section_key[1]] =u'基层动态'
        #会议通知
        self.section_folder_map[self.section_key[2]] =u'会议通知'
        #本部新闻
        self.section_folder_map[self.section_key[3]] =u'本部新闻'
        #企业信息
        self.section_folder_map[self.section_key[4]] =u'企业信息'
        # self.init_mkdir_folder()


    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        self.cur_page = page_num
        article_list = []
        if page_num == 0:
            url = self.section_url_map[section_name]
        else:
            nPos = self.section_url_map[section_name].index('nowPage=')
            url = self.section_url_map[section_name][0:nPos] + 'nowPage=' + str( self.cur_page ) + self.section_url_map[section_name][nPos+len('nowPage=')+1:]

        contentHtml = self.session.get(url, stream=True)
        if contentHtml.status_code == requests.codes.ok:
            pattern = r'<td align="left" width="62%" height="24"><a\s*?href="(.*?)".*?>(.*?)</a>\s.*?<td align="right" width="\d{2}%" height="\d{2}".*?>(.*?)</td>'
            for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                if mtFind.groups()[0][0:4] == "http":
                    article_url = mtFind.groups()[0]
                else:
                    proto, rest = urllib.splittype( self.section_url_map[section_name])
                    article_url = proto + "://" + urllib.splithost( rest )[0] + "/" + mtFind.groups()[0][1:]

                public_time = mtFind.groups()[2].strip('&nbsp;')
                if contentHtml.encoding == 'UTF-8':
                    title = mtFind.groups()[1].decode('UTF-8').strip()
                #print repr(title.decode('UTF-8'))

                item = article_item(article_url, title, public_time)
                item.set_section_name(section_name)
                article_list.append(item)
        else:
            self.logger.error(u'没有获取到文章列表 ' + str(page_num))
        return article_list


if __name__ == '__main__':
    liaoning_spider = liaoningSpider()
    liaoning_spider.init_log(u'辽宁.log')
    liaoning_spider.set_save_folder_path(globalconf.save_folder['liaoning'])
    liaoning_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['liaoning']
    liaoning_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in liaoning_spider.section_key:
        liaoning_spider.logger.info(u"获取栏目:" + section_item + ":" + liaoning_spider.section_folder_map[section_item])
        for page_num in range(liaoning_spider.page_number):
            article_list = liaoning_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                liaoning_spider.stripy_article_context(item)








