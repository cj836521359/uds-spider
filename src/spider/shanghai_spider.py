# -*- coding: utf-8 -*-
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
import urllib
import PyV8
import jsEngineMgr
import globalconf



class shanghaiSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = 'http://www.sh.sgcc.com.cn/sdnw2010/'
        # self.logger = login.initLog('xz.log')
        print 'shanghaiSpider'
        self.session = self.init_session()
        self.folder_base = u'上海'

        js_str = common_utils.read_file_content('shanghai.js')
        self.jsEngineMgr = jsEngineMgr.initJsEngine()
        self.jsShowMenu2 = self.jsEngineMgr.eval(js_str.encode('utf-8'))


        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}

        self.section_key = [
            #国网要闻
            'gwxw',
            #公司要闻
            'gsyw',
            #本部新闻
            'bbxw',
            #基层信息
            'jcxx',
            #媒体报道
            'mtbd',
            #行业资讯
            'hyzx',
        ]




        #国网要闻
        self.section_url_map[self.section_key[0]] = 'http://www.sh.sgcc.com.cn/sdnw2010/load.loadPage.d?page=sub.xml&siteCode=sdnw&urlChannelId=MjE5NDU3NjE%3D'
        #公司要闻
        self.section_url_map[self.section_key[1]] = 'http://www.sh.sgcc.com.cn/sdnw2010/load.loadPage.d?page=sub_gsyw.xml&siteCode=sdnw'
        #本部新闻
        self.section_url_map[self.section_key[2]] = 'http://www.sh.sgcc.com.cn/sdnw2010/load.loadPage.d?page=sub.xml&siteCode=sdnw&urlChannelId=MTAwMTg0'
        #基层信息
        self.section_url_map[self.section_key[3]] = 'http://www.sh.sgcc.com.cn/sdnw2010/load.loadPage.d?page=sub.xml&siteCode=sdnw&urlChannelId=MTAwMTg3'
        #媒体报道
        self.section_url_map[self.section_key[4]] = 'http://www.sh.sgcc.com.cn/sdnw2010/load.loadPage.d?page=sub.xml&siteCode=sdnw&urlChannelId=MTAwMTg1'
        #行业资讯
        self.section_url_map[self.section_key[5]] = 'http://www.sh.sgcc.com.cn/sdnw2010/load.loadPage.d?page=sub.xml&siteCode=sdnw&urlChannelId=MTAwMTg2'




        #国网要闻
        self.section_folder_map[self.section_key[0]] = u'国网要闻'
        #公司要闻
        self.section_folder_map[self.section_key[1]] = u'公司要闻'
        #本部新闻
        self.section_folder_map[self.section_key[2]] = u'本部新闻'
        #基层信息
        self.section_folder_map[self.section_key[3]] = u'基层信息'
        #媒体报道
        self.section_folder_map[self.section_key[4]] = u'媒体报道'
        #行业资讯
        self.section_folder_map[self.section_key[5]] = u'行业资讯'




    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        self.cur_page = page_num
        self.logger.info(self.cur_page)
        article_list = []
        data = "pageIndex=" + str(self.cur_page)
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        contentHtml = self.session.post(self.section_url_map[section_name], data=data, headers=headers)
        #print contentHtml.content

        if contentHtml.status_code == requests.codes.ok:
            pattern = "onclick=\"showMenus2\('(\d*)','(\d*)','(\d*)'.*?>(.*?)</a>\s.*?<td.*?\[(.*?)\]"
            for mtFind in re.finditer(pattern ,contentHtml.text,re.S):
                title = mtFind.groups()[3].strip('\r\n\t')
                article_url = self.url_base + self.jsShowMenu2(mtFind.groups()[0], mtFind.groups()[1], mtFind.groups()[2])
                public_time = mtFind.groups()[4]
                print title
                print public_time
                print article_url
                item = article_item(article_url, title, public_time)
                item.set_section_name(section_name)
                article_list.append(item)

        else:
            self.logger.error(u'没有获取到文章列表 ' + str(page_num))

        return article_list

    #爬取文章内容
    #上海需要重新写 爬取,因为没有
    def stripy_article_context( self, article_item ):
        self.logger.info(u"爬取文章")
        self.logger.info(article_item.article_url)
        self.logger.info(article_item.title)
        self.logger.info(article_item.public_time)

        title = article_item.title
        for rstr in common_utils.replace_str:
            if rstr in title:
                title = title.replace( rstr, "" )
        title.strip()

        #获取扩展名
        ext = '.shtml'
        findExt = False
        for extType in common_utils.down_type:
            if extType in ext:
                findExt = True
                break

        file_name = self.folder_base + '/' + self.section_folder_map[article_item.section_name] + '/' + str( self.cur_page ) + '_' + article_item.public_time + '_' + title
        if findExt == True:
            file_name = self.save_folder + file_name + ext
        else:
            file_name = self.save_folder + file_name + ".shtml"

        #print file_name
        #sys.exit(1)


        #try:
        contentHtml = self.session.get( article_item.article_url, stream=True )
        #common_utils.write_to_file_with_stream( contentHtml.content,'nmgggg.txt')
        pattern = r'([^\x00-\xff]{4,5})[\]\s]*(\d{4}-\d{2}-\d{2})'
        r = re.search(pattern,contentHtml.text,re.S)
        if r:
            pubdt = r.group(2)
            if self.is_in_date(pubdt) == False:
                return
            #if time.strptime( pubdt, '%Y-%m-%d' ).tm_year != 2015:
                #self.logger.error(u'不下载 发布时间:' + pubdt + 'u' + article_item.title)
                #return

        if contentHtml.status_code == requests.codes.ok:
            self.logger.info( u'返回成功')
            common_utils.write_to_file_with_stream( contentHtml.content, file_name)
        else:
            self.logger.error(u'下载失败!!!:' + file_name)




if __name__ == '__main__':
    js_str = common_utils.read_file_content('shanghai.js')
    shanghai_spider = shanghaiSpider()
    shanghai_spider.init_log(u'上海.log')
    shanghai_spider.jsEngineMgr = jsEngineMgr.initJsEngine()
    shanghai_spider.jsShowMenu2 = shanghai_spider.jsEngineMgr.eval(js_str.encode('utf-8'))
    shanghai_spider.set_save_folder_path(globalconf.save_folder['shanghai'])
    shanghai_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['shanghai']
    shanghai_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])

    for section_item in shanghai_spider.section_key:
        shanghai_spider.logger.info(u"获取栏目:" + section_item + ":" + shanghai_spider.section_folder_map[section_item])
        for page_num in range(shanghai_spider.page_number):
            article_list = shanghai_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                shanghai_spider.stripy_article_context(item)
