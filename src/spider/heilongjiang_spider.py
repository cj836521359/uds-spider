# -*- coding: utf-8 -*-
__author__ = 'chencharles'
#import spider
from spider import *
import sys
import time
import chardet
import urllib


class heilongjiangSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        # self.logger = login.initLog('hlj.log')
        print 'heilongjiangSpider'
        self.session = self.init_session()
        self.folder_base = u'黑龙江'
        self.page_number = 10

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}

        self.section_key = [
            #公司要闻
            'gsyw',
            #媒体报道
            'mtbd',
            #基层动态
            'jcdt',
            #科技信息-工作动态
            'kjxx_gzdt',
            #科技信息-工作成果
            'kjxx_gzcg',
            #营销服务-政策法规
            'yxfw_zcfg',
            #营销服务-工作动态
            'yxfw_gzdt',
            #农村电力-农电信息
            'ncdl_ndxx',
            #农村电力-农网发展
            'ncdl_nwfz',
            #农村电力-农电服务
            'ncdl_ndfw',
            #政工工作-工作部署
            'zggz_gzbs',
            #政工工作-工作部署
            'zggz_gzbs',
            #政工工作-制度规范
            'zggz_zdgf',
            #政工工作-基层实践
            'zggz_zcsj',
            #电网建设-工程动态
            'dwjs_gcdt',
            #电网建设-标准规范
            'dwjs_bzgf',
            #电网建设-安全质量
            'dwjs_aqzl',
            #电网建设-“基建安全质量年”活动专栏
            'dwjs_hdzl',
            #安全保卫
            'aqbw',
            #安全信息
            'aqxx',
            ]


        # {
        #     "key": "黑龙江",
        #     "name":"heilongjiang",
        #     "limit_date":"20150101-20150101",
        #     "sections": [
        #         {"gsyw":{"spider":true,"name":"公司要闻"}},
        #         {"mtbd":{"spider":true,"name":"媒体报道"}},
        #         {"jcdt":{"spider":true,"name":"基层动态"}},
        #         {"kjxx_gzdt":{"spider":true,"name":"科技信息-工作动态"}},
        #         {"kjxx_gzcg":{"spider":true,"name":"科技信息-工作成果"}},
        #         {"yxfw_zcfg":{"spider":true,"name":"营销服务-政策法规"}},
        #         {"yxfw_gzdt":{"spider":true,"name":"营销服务-工作动态"}},
        #         {"ncdl_ndxx":{"spider":true,"name":"农村电力-农电信息"}},
        #         {"ncdl_nwfz":{"spider":true,"name":"农村电力-农网发展"}},
        #         {"ncdl_ndfw":{"spider":true,"name":"农村电力-农电服务"}},
        #         {"zggz_gzbs":{"spider":true,"name":"政工工作-工作部署"}},
        #         {"zggz_gzbs":{"spider":true,"name":"政工工作-工作部署"}},
        #         {"zggz_zdgf":{"spider":true,"name":"政工工作-制度规范"}},
        #         {"zggz_zcsj":{"spider":true,"name":"政工工作-基层实践"}},
        #         {"dwjs_gcdt":{"spider":true,"name":"电网建设-工程动态"}},
        #         {"dwjs_bzgf":{"spider":true,"name":"电网建设-标准规范"}},
        #         {"dwjs_aqzl":{"spider":true,"name":"电网建设-安全质量"}},
        #         {"dwjs_hdzl":{"spider":true,"name":"电网建设-基建安全质量年活动专栏"}},
        #         {"aqbw":{"spider":true,"name":"安全保卫"}},
        #         {"aqxx":{"spider":true,"name":"安全信息"}}
        #     ]
        # }




        #公司要闻
        self.section_url_map[self.section_key[0]] = 'http://10.166.4.100/sy/gsyw/index.shtml'
        #媒体报道
        self.section_url_map[self.section_key[1]] = 'http://10.166.4.100/mtgz/index.shtml'
        #基层动态
        self.section_url_map[self.section_key[2]] = 'http://10.166.4.100/sy/jcdt/index.shtml'
        #科技信息-工作动态
        self.section_url_map[self.section_key[3]] = 'http://10.166.4.100/kjxx/gzdt/index.shtml'
        #科技信息-工作成果
        self.section_url_map[self.section_key[4]] = 'http://10.166.4.100/kjxx/kjcg/index.shtml'
        #营销服务-政策法规
        self.section_url_map[self.section_key[5]] = 'http://10.166.4.100/yxfw/zcfg/index.shtml'
        #营销服务-工作动态
        self.section_url_map[self.section_key[6]] = 'http://10.166.4.100/yxfw/gzdt/index.shtml'
        #农村电力-农电信息
        self.section_url_map[self.section_key[7]] = 'http://10.166.4.100/sy/ncdl/ndxx/index.shtml'
        #农村电力-农网发展
        self.section_url_map[self.section_key[8]] = 'http://10.166.4.100/sy/ncdl/nwfz/index.shtml'
        #农村电力-农电服务
        self.section_url_map[self.section_key[9]] = 'http://10.166.4.100/sy/ncdl/ndfw/index.shtml'
        #政工工作-工作部署
        self.section_url_map[self.section_key[10]] = 'http://10.166.4.100/zggz/gzbs/index.shtml'
        #政工工作-工作部署
        self.section_url_map[self.section_key[11]] = 'http://10.166.4.100/zggz/gzbs/index.shtml'
        #政工工作-制度规范
        self.section_url_map[self.section_key[12]] = 'http://10.166.4.100/zggz/zdgf/index.shtml'
        #政工工作-基层实践
        self.section_url_map[self.section_key[13]] = 'http://10.166.4.100/zggz/jcsj/index.shtml'
        #电网建设-工程动态
        self.section_url_map[self.section_key[14]] = 'http://10.166.4.100/sy/dwjs/dwjs/gcdt/index.shtml'
        #电网建设-标准规范
        self.section_url_map[self.section_key[15]] = 'http://10.166.4.100/sy/dwjs/dwjs/bzgf/index.shtml'
        #电网建设-安全质量
        self.section_url_map[self.section_key[16]] = 'http://10.166.4.100/sy/dwjs/dwjs/aqzl/index.shtml'
        #电网建设-“基建安全质量年”活动专栏
        self.section_url_map[self.section_key[17]] = 'http://10.166.4.100/sy/dwjs/dwjs/_jjaqzln_hdzl/index.shtml'
        #安全保卫
        self.section_url_map[self.section_key[18]] = 'http://10.166.4.100/sy/aqsc/aqbw/index.shtml'
        #安全信息
        self.section_url_map[self.section_key[19]] = 'http://10.166.4.100/sy/aqsc/aqxx/index.shtml'

        #公司要闻
        self.section_folder_map[self.section_key[0]] = u'公司要闻'
        #媒体报道
        self.section_folder_map[self.section_key[1]] = u'媒体报道'
        #基层动态
        self.section_folder_map[self.section_key[2]] = u'基层动态'
        #科技信息-工作动态
        self.section_folder_map[self.section_key[3]] = u'科技信息-工作动态'
        #科技信息-工作成果
        self.section_folder_map[self.section_key[4]] = u'科技信息-工作成果'
        #营销服务-政策法规
        self.section_folder_map[self.section_key[5]] = u'营销服务-政策法规'
        #营销服务-工作动态
        self.section_folder_map[self.section_key[6]] = u'营销服务-工作动态'
        #农村电力-农电信息
        self.section_folder_map[self.section_key[7]] = u'农村电力-农电信息'
        #农村电力-农网发展
        self.section_folder_map[self.section_key[8]] = u'农村电力-农网发展 '
        #农村电力-农电服务
        self.section_folder_map[self.section_key[9]] = u'农村电力-农电服务'
        #政工工作-工作部署
        self.section_folder_map[self.section_key[10]] = u'政工工作-工作部署'
        #政工工作-工作部署
        self.section_folder_map[self.section_key[11]] = u'政工工作-工作部署'
        #政工工作-制度规范
        self.section_folder_map[self.section_key[12]] = u'政工工作-制度规范'
        #政工工作-基层实践
        self.section_folder_map[self.section_key[13]] = u'政工工作-基层实践'
        #电网建设-工程动态
        self.section_folder_map[self.section_key[14]] = u'电网建设-工程动态'
        #电网建设-标准规范
        self.section_folder_map[self.section_key[15]] = u'电网建设-标准规范'
        #电网建设-安全质量
        self.section_folder_map[self.section_key[16]] = u'电网建设-安全质量 '
        #电网建设-基建安全质量年-活动专栏
        self.section_folder_map[self.section_key[17]] = u'电网建设-基建安全质量年-活动专栏'
        #安全保卫
        self.section_folder_map[self.section_key[18]] = u'安全保卫'
        #安全信息
        self.section_folder_map[self.section_key[19]] = u'安全信息'
        # self.init_mkdir_folder()


    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-6] + '_' + str(self.cur_page) + '.shtml'
                #nPos = self.section_url_map[section_name].index('nowPage=')
                #url = self.section_url_map[section_name][0:nPos] + 'nowPage=' + str( self.cur_page ) + self.section_url_map[section_name][nPos+len('nowPage=')+1:]
            print url

            contentHtml = self.session.get(url, stream=True)
            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<a class=\'xwbtlink1\'.*?href="(.*?)">(.*?)</a>.*?</td>\s.*?<td.*?>(.*?)</td>'
                for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        proto,rest = urllib.splittype( self.section_url_map[section_name])
                        article_url = proto + "://" + urllib.splithost(rest)[0] + "/" + mtFind.groups()[0][1:]

                    public_time = self.strip_tags(mtFind.groups()[2])

                    encoding = chardet.detect(contentHtml.content)['encoding']
                    title = mtFind.groups()[1].decode(encoding)
                    item = article_item(article_url, title, public_time)
                    item.set_section_name(section_name)
                    article_list.append(item)
                print mtFind.groups()
            else:
                self.logger.error(u'没有获取到文章列表 ' + str(page_num) )
        except BaseException, e:
            self.logger.error(str(e))
        finally:
            return article_list


if __name__ == '__main__':
    # hlj_spider = heilongjiangSpider()
    #
    # for k,v in hlj_spider.section_url_map.items():
    #     hlj_spider.logger.info(u'获取栏目:' + k + ":" +  hlj_spider.section_folder_map[k] )
    #     for page_num in range( hlj_spider.page_number ):
    #         article_list = hlj_spider.stripy_article_list( k , page_num )
    #         for item in article_list:
    #             hlj_spider.stripy_article_context( item )

    heilongjiang_spider = heilongjiangSpider()
    heilongjiang_spider.init_log(u'黑龙江.log')

    heilongjiang_spider.set_save_folder_path(globalconf.save_folder['heilongjiang'])
    heilongjiang_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['heilongjiang']
    heilongjiang_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])

    for section_item in heilongjiang_spider.section_key:
        heilongjiang_spider.logger.info(u"获取栏目:" + section_item + ":" + heilongjiang_spider.section_folder_map[section_item])
        for page_num in range(heilongjiang_spider.page_number):
            article_list = heilongjiang_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                heilongjiang_spider.stripy_article_context(item)










