# -*- coding: utf-8 -*-
__author__ = 'chencharles'
#import spider
from __init__ import *
from spider import *
import sys
import time
import chardet
import urllib


class neimengguSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        # self.logger = login.initLog('nmg.log')
        print 'neimengguSpider'
        self.session = self.init_session()
        self.folder_base = u'内蒙古'


        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}

        self.section_key = [
            #重要通知
            'zytz',
            #头条新闻
            'ttxw',
            #本部新闻
            'bbxw',
            #基层信息
            'jjxx',
            #媒体报道
            'mtbd',
            #领导讲话
            'ldjh',
            #行业信息
            'hyxx',
        ]


        # 重要通知
        self.section_url_map[self.section_key[0]] = 'http://portal.md.sgcc.com.cn/xwzx/zytz/index.shtml'
        # 头条新闻
        self.section_url_map[self.section_key[1]] = 'http://portal.md.sgcc.com.cn/xwzx/ttxw/index.shtml'
        # 本部新闻
        self.section_url_map[self.section_key[2]] = 'http://portal.md.sgcc.com.cn/xwzx/gsyw/index.shtml'
        # 基层信息
        self.section_url_map[self.section_key[3]] = 'http://portal.md.sgcc.com.cn/xwzx/zsxx/index.shtml'
        # 媒体报道
        self.section_url_map[self.section_key[4]] = 'http://portal.md.sgcc.com.cn/xwzx/mtbd/index.shtml'
        # 领导讲话
        self.section_url_map[self.section_key[5]] = 'http://portal.md.sgcc.com.cn/xwzx/ldjh/index.shtml'
        # 行业信息
        self.section_url_map[self.section_key[6]] = 'http://portal.md.sgcc.com.cn/xwzx/xxck/index.shtml'



        # 重要通知
        self.section_folder_map[self.section_key[0]] = u'重要通知'
        # 头条新闻
        self.section_folder_map[self.section_key[1]] = u'头条新闻'
        # 本部新闻
        self.section_folder_map[self.section_key[2]] = u'本部新闻'
        # 基层信息
        self.section_folder_map[self.section_key[3]] = u'基层信息'
        # 媒体报道
        self.section_folder_map[self.section_key[4]] = u'媒体报道'
        # 领导讲话
        self.section_folder_map[self.section_key[5]] = u'领导讲话'
        # 行业信息
        self.section_folder_map[self.section_key[6]] = u'行业信息'



    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-6] + '_' + str(self.cur_page) + '.shtml'

            contentHtml = self.session.get( url, stream=True )
            encoding = chardet.detect(contentHtml.content)['encoding']

            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<td align="left"><div class=" newstitlesdowngexian">.*?<a href="(.*?)">(.*?)</a>.*?<td>\[(.*?)\]</td>'
                for mtFind in re.finditer( pattern ,contentHtml.content,re.S ):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        proto,rest = urllib.splittype( self.section_url_map[section_name])
                        article_url = proto + "://" + urllib.splithost(rest)[0] + "/" + mtFind.groups()[0][1:]

                    public_time = mtFind.groups()[2].strip('&nbsp;').strip()
                    title = mtFind.groups()[1].decode(encoding).strip()
                    title = self.strip_tags(title)

                    item = article_item(article_url, title, public_time)
                    item.set_section_name(section_name)
                    article_list.append(item)
            else:
                self.logger.error(u'没有获取到文章列表 ' + str(page_num))
        except BaseException, e:
            self.logger.error(str(e))
        finally:
            return article_list



    #爬取文章内容
    def stripy_article_context( self, article_item ):
        self.logger.info( u"爬取文章" )
        self.logger.info( article_item.article_url )
        self.logger.info( article_item.title )
        self.logger.info( article_item.public_time )

        title = article_item.title
        for rstr in common_utils.replace_str:
            if rstr in title:
                title = title.replace( rstr, "" )
        title.strip()

        #获取扩展名
        ext = article_item.article_url.split( "/" )[-1]
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



        try:
            contentHtml = self.session.get( article_item.article_url, stream=True )
            pattern = r'([^\x00-\xff]{4,5})[\]\s]*(\d{2}-\d{2}-\d{2})'
            r = re.search(pattern,contentHtml.text,re.S)
            if r:
                pubdt = "20" + r.group(2)
                if self.is_in_date(pubdt) == False:
                    return

            if contentHtml.status_code == requests.codes.ok:
                self.logger.info( u'返回成功')
                common_utils.write_to_file_with_stream( contentHtml.content , file_name )
            else:
                self.logger.error(u'下载失败!!!:' + file_name )
        except BaseException, e:
            self.logger.error(str(e))



if __name__ == '__main__':
    neimenggu_spider = neimengguSpider()
    neimenggu_spider.init_log(u'内蒙古.log')
    neimenggu_spider.set_save_folder_path(globalconf.save_folder['neimenggu'])
    neimenggu_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['neimenggu']
    neimenggu_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in neimenggu_spider.section_key:
        neimenggu_spider.logger.info(u"获取栏目:" + section_item + ":" + neimenggu_spider.section_folder_map[section_item])
        for page_num in range(neimenggu_spider.page_number):
            article_list = neimenggu_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                neimenggu_spider.stripy_article_context(item)










