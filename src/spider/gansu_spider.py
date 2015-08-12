
# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
import urllib

class gansuSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = 'http://portal1.gs.sgcc.com.cn/'
        # self.logger = login.initLog('sx.log')
        print 'gansuSpider'
        self.session = self.init_session()
        self.folder_base = u'甘肃'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            #国网动态
            'gwdt',
            #公司新闻
            'gsxw',
            #基层动态
            'jcdt',
            #本部新闻
            'bbxw',
            #媒体报道
            'mtbd'
        ]

        # {
        #     "key": "gansu",
        #     "name":"甘肃",
        #     "limit_date":"20150101-20150101",
        #     "sections": [
        #         {"gwdt":{"spider":true,"name":"国网动态"}},
        #         {"gsxw":{"spider":true,"name":"公司新闻"}},
        #         {"jcdt":{"spider":true,"name":"基层动态"}},
        #         {"bbxw":{"spider":true,"name":"本部新闻"}},
        #         {"mtbd":{"spider":true,"name":"媒体报道"}}
        #     ]
        # }

        #国网动态
        self.section_url_map[self.section_key[0]] = 'http://portal1.gs.sgcc.com.cn/view_list.action?page=1&classid=3711'
        #公司新闻
        self.section_url_map[self.section_key[1]] = 'http://portal1.gs.sgcc.com.cn/view_list.action?page=1&classid=5'
        #基层动态
        self.section_url_map[self.section_key[2]] = 'http://portal1.gs.sgcc.com.cn/view_list.action?page=1&classid=7'
        #本部新闻
        self.section_url_map[self.section_key[3]] = 'http://portal1.gs.sgcc.com.cn/view_list.action?page=1&classid=2665'
        #媒体报道
        self.section_url_map[self.section_key[4]] = 'http://portal1.gs.sgcc.com.cn/view_list.action?page=1&classid=8'


        #国网动态
        self.section_folder_map[self.section_key[0]] = u'国网动态'
        #公司新闻
        self.section_folder_map[self.section_key[1]] = u'公司新闻'
        #基层动态
        self.section_folder_map[self.section_key[2]] = u'基层动态'
        #本部新闻
        self.section_folder_map[self.section_key[3]] = u'本部新闻'
        #媒体报道
        self.section_folder_map[self.section_key[4]] = u'媒体报道'



        #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        self.cur_page = page_num
        article_list = []
        url = re.sub(r'page=\d', 'page='+str(page_num), self.section_url_map[section_name])
        self.logger.info(url)

        contentHtml = self.session.get(url)
        encoding = chardet.detect(contentHtml.content)['encoding']
        #if contentHtml.encoding == 'ISO-8859-1':
            #contentHtml.encoding = 'gbk'
        #else:
            #contentHtml.encoding = 'utf-8'

        if contentHtml.status_code == requests.codes.ok:
            pattern = r'<a href="(view_info.*?)" target="_blank" title=[\s\S]+?>(.*?)</a>\s.*?style="text-align:center">(.{8})'
            #pattern = r'<a href="(view_info.*?)" target=.* title=.+?>(.*?)</a>'
            for mtFind in re.finditer(pattern, contentHtml.text, re.S):
                if mtFind.groups()[0][0:4] == "http":
                    article_url = mtFind.groups()[0]
                else:
                    article_url = '%s%s' %(self.url_base, mtFind.groups()[0])
                title = mtFind.groups()[1].strip('\r\n\t')
                #获取到的年份是15/04/15,所以前面加20,构成2015/04/15
                public_time = time.strptime('20'+mtFind.groups()[2],'%Y/%m/%d')
                public_time = time.strftime('%Y-%m-%d',public_time)

                item = article_item(article_url, title, public_time)
                item.set_section_name(section_name)
                article_list.append(item)

        else:
            logger.error(u'没有获取到文章列表 ' + str(pageNum) )
        return article_list





# def stripy_article_context( contentUrl, sectionName, title ):
#     #ext = os.path.splitext(contentUrl)[1]
#     #logger.info(title)
#
#     title=title.replace("\\","")
#     title=title.replace("/","")
#     title=title.replace("\"","")
#     title=title.replace(":","")
#     title=title.replace("*","")
#     title=title.replace("?","")
#     title=title.replace("","")
#     title=title.replace("<","")
#     title=title.replace(">","")
#     title=title.replace("|","")
#     title=title.replace("	","")
#     title.strip()
#     #replaceStr=["\\","/",":",":","*","?","\","<",">","|"]
#
#     logger.info(title)
#
#
#     fileName = folderbase + '/' + folderMap[sectionName] + '/' + str(cur_page) + '_' + title + '.shtml'
#     logger.info( contentUrl )
#     logger.info( fileName )
#     contentHtml = session.get(contentUrl)
#
#     #===============================
#     if contentHtml.encoding == 'ISO-8859-1':
#         contentHtml.encoding = 'gbk'
#     else:
#         contentHtml.encoding = 'utf-8'
#     if contentHtml.status_code == 200:
#         logger.info( u'返回成功')
#         common_utils.write_to_file( contentHtml.text, fileName )
#         #with open(fileName,'wb') as f:
#         #f.write( contentHtml.text )
#         #f.close()
#     else:
#         logger.error(u'下载失败!!!:' + fileName )





if __name__ == '__main__':
    # logger = login.initLog('jl.log')
    # init() #创建文件夹
    # session = initSession()
    # #for pageNum in range(15,16):
    # for k,v in sectionMap.items():
    #     logger.info(u'获取栏目:' + k)
    #     for pageNum in range(1,pageNumber):
    #         #for pageNum in range(8,9):
    #         articleList = stripy_article_list( k ,  pageNum )
    #         for (url,title) in articleList:
    #             stripy_article_context( url, k , title )
    #
    #             #for pageNum in range(pageNumber):
    #             ##for pageNum in range(8,9):
    #             #articleList = stripy_article_list( 'mtbd' ,  pageNum )
    #             #for (url,title) in articleList:
    #             #stripy_article_context( url, 'mtbd' , title )
    gansu_spider = gansuSpider()
    gansu_spider.init_log(u'甘肃.log')
    gansu_spider.set_save_folder_path(globalconf.save_folder['gansu'])
    gansu_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['gansu']
    gansu_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])

    for section_item in gansu_spider.section_key:
        gansu_spider.logger.info(u"获取栏目:" + section_item + ":" + gansu_spider.section_folder_map[section_item])
        for page_num in range(gansu_spider.page_number):
            article_list = gansu_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                gansu_spider.stripy_article_context(item)

