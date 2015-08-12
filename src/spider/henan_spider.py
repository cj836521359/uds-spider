# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
import urllib


class henanSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        # self.logger = login.initLog('hn.log')
        print 'henspider'
        self.session = self.init_session()
        self.folder_base = u'河南'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            # 公司新闻
            'gsxw',
            # 市公司动态
            'jcdt_sgs',
            # 县公司动态
            'jcdt_xgs',
            # 媒体报道
            'mtbd',
            ]

        # {
        #     "key": "河南",
        #     "name":"henan",
        #     "limit_date":"20150101-20150101",
        #     "sections": [
        #
        #         {"gsxw":{"spider":true,"name":"公司新闻"}},
        #         {"jcdt_sgs":{"spider":true,"name":"市公司动态"}},
        #         {"jcdt_xgs":{"spider":true,"name":"县公司动态"}},
        #         {"mtbd":{"spider":true,"name":"媒体报道"}}
        #
        #         ]
        # }


        #公司新闻
        self.section_url_map[self.section_key[0]] = 'http://system.ha.sgcc.com.cn/portal/gsxw/A0702index_1.htm'
        #市公司动态
        self.section_url_map[self.section_key[1]] = 'http://system.ha.sgcc.com.cn/portal/jcdt/sgs/A070301index_1.htm'
        #县公司动态
        self.section_url_map[self.section_key[2]] = 'http://system.ha.sgcc.com.cn/portal/jcdt/xgs/A070302index_1.htm'
        #媒体报道
        self.section_url_map[self.section_key[3]] = 'http://system.ha.sgcc.com.cn/portal/mtbd/A0718index_1.htm'



        #公司新闻
        self.section_folder_map[self.section_key[0]] = u'公司新闻'
        #基层动态 市公司动态
        self.section_folder_map[self.section_key[1]] = u'基层动态_市公司动态'
        #基层动态 县公司动态
        self.section_folder_map[self.section_key[2]] = u'基层动态_县公司动态'
        #媒体报道
        self.section_folder_map[self.section_key[3]] = u'媒体报道'
        # self.init_mkdir_folder()



    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                #url = self.section_url_map[section_name] + 'index_' + str(self.cur_page) + '.htm'
                url = self.section_url_map[section_name][0:-5] + str( self.cur_page ) + '.htm'

                #nPos = self.section_url_map[section_name].index('nowPage=')
                #url = self.section_url_map[section_name][0:nPos] + 'nowPage=' + str( self.cur_page ) + self.section_url_map[section_name][nPos+len('nowPage=')+1:]
                #print url
                #sys.exit(1)

            contentHtml = self.session.get(url, stream=True)
            encoding = chardet.detect(contentHtml.content)['encoding']

            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<SPAN>\[(.*?)\]</SPAN><A .*?href=(.*?) target=_blank>(.*?)</A><SCRIPT>'
                for mtFind in re.finditer( pattern ,contentHtml.content,re.S ):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        proto,rest = urllib.splittype( self.section_url_map[section_name])
                        article_url = proto + "://" + urllib.splithost( rest )[0] + "/" + mtFind.groups()[1][1:]
                        #article_url = self.section_url_map[section_name][1:] + mtFind.groups()[1][1:]
                        #print "ss"
                        #print article_url
                        #sys.exit(1)


                    public_time = self.strip_tags(mtFind.groups()[0])
                    #print public_time
                    #sys.exit(1)

                    title = mtFind.groups()[2].decode(encoding)


                    #print repr(title)
                    #print title
                    #print article_url
                    #sys.exit(1)

                    item = article_item( article_url,title, public_time )
                    item.set_section_name( section_name )
                    article_list.append( item )
            else:
                self.logger.error(u'没有获取到文章列表 ' + str(page_num) )
        except BaseException, e:
            self.logger.error(str(e))
        finally:
            return article_list



if __name__ == '__main__':
    henan_spider = henanSpider()
    henan_spider.init_log(u'河南.log')
    henan_spider.set_save_folder_path(globalconf.save_folder['henan'])
    henan_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['henan']
    henan_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in henan_spider.section_key:
        henan_spider.logger.info(u"获取栏目:" + section_item + ":" + henan_spider.section_folder_map[section_item])
        for page_num in range(henan_spider.page_number):
            article_list = henan_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                henan_spider.stripy_article_context(item)















