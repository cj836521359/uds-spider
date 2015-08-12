# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet

class hubeiSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        # self.logger = login.initLog('hub.log')
        print 'hubeiSpider'
        self.session = self.init_session()
        self.folder_base = u'湖北'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            # 公司要闻
            'gsyw',
            # 领导讲话
            'ldjh',
            # 本部动态
            'bbdt',
            # 媒体报道
            'mtbd',
            # 工作交流
            'gzjl',
            # 工作研究
            'gzyj',
            # 一线风采
            'yxfc',
            ]

        # {
        #     "key": "湖北",
        #     "name":"hubei",
        #     "limit_date":"20150101-20150101",
        #     "sections": [
        #         {"gsyw":{"spider":true,"name":"公司要闻"}},
        #         {"ldjh":{"spider":true,"name":"领导讲话"}},
        #         {"bbdt":{"spider":true,"name":"本部动态"}},
        #         {"mtbd":{"spider":true,"name":"媒体报道"}},
        #         {"gzjl":{"spider":true,"name":"工作交流"}},
        #         {"gzyj":{"spider":true,"name":"工作研究"}},
        #         {"yxfc":{"spider":true,"name":"一线风采"}}
        #         ]
        # }
        self.section_url_map[self.section_key[0]] = 'http://10.228.0.2/news/1004/1021/index.html'
        self.section_url_map[self.section_key[1]] = 'http://10.228.0.2/news/1004/1022/index.html'
        self.section_url_map[self.section_key[2]] = 'http://10.228.0.2/news/1004/1023/index.html'
        self.section_url_map[self.section_key[3]] = 'http://10.228.0.2/news/1004/1025/index.html'
        self.section_url_map[self.section_key[4]] = 'http://10.228.0.2/news/1004/2649/index.html'
        self.section_url_map[self.section_key[5]] = 'http://10.228.0.2/news/1004/1027/index.html'
        self.section_url_map[self.section_key[6]] = 'http://10.228.0.2/news/1004/2650/index.html'


        # 公司要闻
        self.section_folder_map[self.section_key[0]] = u'公司要闻'
        # 领导讲话
        self.section_folder_map[self.section_key[1]] = u'领导讲话'
        # 本部动态
        self.section_folder_map[self.section_key[2]] = u'本部动态'
        # 媒体报道
        self.section_folder_map[self.section_key[3]] = u'媒体报道'
        # 工作交流
        self.section_folder_map[self.section_key[4]] = u'工作交流'
        # 工作研究
        self.section_folder_map[self.section_key[5]] = u'工作研究'
        # 一线风采
        self.section_folder_map[self.section_key[6]] = u'一线风采'



    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            contentHtml = None
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-10] + '/' + 'pages/index_' + str(self.cur_page) + '.html'

            contentHtml = self.session.get(url, stream=True)
            encoding = chardet.detect(contentHtml.content)['encoding']

            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<td width="85%" height="30" class="title".*?<A\s.*?href="(.*?)".*?>(.*?)</A></td>.*?>(.*?)</td>'
                for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        article_url = '%s%s' %(self.section_url_map[section_name][0:18], mtFind.groups()[0][1:])

                    public_time = mtFind.groups()[2]

                    title = mtFind.groups()[1]
                    title = title.decode(encoding).strip()

                    item = article_item(article_url, title, public_time)
                    item.set_section_name(section_name)
                    article_list.append(item)
            else:
                self.logger.error(u'没有获取到文章列表 ' + str(page_num))
        except BaseException, e:
            self.logger.error(str(e))
        finally:
            return article_list


if __name__ == '__main__':
    hubei_spider = hubeiSpider()
    hubei_spider.init_log(u'湖北.log')
    hubei_spider.set_save_folder_path(globalconf.save_folder['hubei'])
    hubei_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['hubei']
    hubei_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])

    for section_item in hubei_spider.section_key:
        hubei_spider.logger.info(u"获取栏目:" + section_item + ":" + hubei_spider.section_folder_map[section_item])
        for page_num in range(hubei_spider.page_number):
            article_list = hubei_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                hubei_spider.stripy_article_context(item)






