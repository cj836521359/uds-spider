#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'chencharles'

from __init__ import *
from spider import *
import chardet
import demjson
import time


class shandongSpider(spiderBase):
    def __init__(self):
        self.url_base = 'http://portal.sd.sgcc.com.cn/opencms/opencms'
        self.page_number = 100
        self.session = self.init_session()
        self.folder_base = u'山东'
        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}

        self.section_key = [
            # 公司要闻
            'gsyw',
            # 本部新闻
            'bbxw',
            # 媒体报道
            'mtbd',
            # 基层动态 市基层
            'jcdt_sjc',
            # 基层动态 省供电公司
            'jcdt_xjc',
            ]



        self.section_url_map[self.section_key[0]] = 'http://portal.sd.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        self.section_url_map[self.section_key[1]] = 'http://portal.sd.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        self.section_url_map[self.section_key[2]] = 'http://portal.sd.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        self.section_url_map[self.section_key[3]] = 'http://portal.sd.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        self.section_url_map[self.section_key[4]] = 'http://portal.sd.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'


        # 公司要闻
        self.section_folder_map[self.section_key[0]] = u'公司要闻'
        # 本部新闻
        self.section_folder_map[self.section_key[1]] = u'本部新闻'
        # 媒体报道
        self.section_folder_map[self.section_key[2]] = u'媒体报道'
        # 基层动态 市基层
        self.section_folder_map[self.section_key[3]] = u'市基层'
        # 基层动态 省供电公司
        self.section_folder_map[self.section_key[4]] = u'省供电公司'



        # 公司要闻
        self.post_data_map[self.section_key[0]] ='status=P&page=%s&id=00001334'
        # 本部新闻
        self.post_data_map[self.section_key[1]] ='status=P&page=%s&id=00001335'
        # 媒体报道
        self.post_data_map[self.section_key[2]] ='status=P&page=%s&id=00001337'
        # 基层动态 市基层
        self.post_data_map[self.section_key[3]] ='status=P&page=%s&id=00001336&id=00001336'
        # 基层动态 省供电公司
        self.post_data_map[self.section_key[4]] ='status=P&page=%s&id=00002224'




        # 公司要闻
        self.referer_map[self.section_key[0]] = 'http://portal.sd.sgcc.com.cn/opencms/opencms/jsp/shandong/portletMore_v3_ln.jsp?path=/opencms/opencms/jsp/shandong/portletMore_v3_new.jsp?id=00001334&child=false&offset=-7&style='
        # 本部新闻
        self.referer_map[self.section_key[1]] = 'http://portal.sd.sgcc.com.cn/opencms/opencms/jsp/shandong/portletMore_v3_ln.jsp?path=/opencms/opencms/jsp/shandong/portletMore_v3_new.jsp?id=00001335&child=false&offset=-7&style='
        # 媒体报道
        self.referer_map[self.section_key[2]] = 'http://portal.sd.sgcc.com.cn/opencms/opencms/jsp/shandong/portletMore_v3_ln.jsp?path=/opencms/opencms/jsp/shandong/portletMore_v3_new.jsp?id=00001335&child=false&offset=-7&style='
        # 基层动态 市基层
        self.referer_map[self.section_key[3]] = 'http://portal.sd.sgcc.com.cn/opencms/opencms/jsp/shandong/portletMore_v3.jsp?id=00001336&?&id=00001336&child=false&offset=-7&style='
        self.referer_map[self.section_key[4]] = 'http://portal.sd.sgcc.com.cn/opencms/opencms/jsp/shandong/portletMore_v3.jsp?&id=00002224&child=false&offset=-7&style='






    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        self.cur_page = page_num
        self.logger.info(self.cur_page)
        article_list = []
        headers = \
            {'Content-Type': 'application/x-www-form-urlencoded', 'referer': self.referer_map[section_name]}
        data = self.post_data_map[section_name] %(self.cur_page)
        self.logger.info(data)

        # url = 'http://portal.sd.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        url = self.section_url_map[section_name]
        contentHtml = self.session.post(url, data=data, headers=headers)
        encoding = chardet.detect(contentHtml.content)['encoding']

        if contentHtml.status_code == 200:
            jsonDic = demjson.decode(contentHtml.text)

            for topiccontents in jsonDic['topiccontents']:
                title = topiccontents['title']
                filename = topiccontents['filename']
                url = topiccontents['url']
                createdate = time.strptime(topiccontents['createdate'],"%Y/%m/%d %H:%M:%S")
                createdate = time.strftime('%Y-%m-%d',createdate)
                if url == "":
                    articleUrl = '%s%s' %(self.url_base, filename)
                else:
                    articleUrl = url
                print title
                print articleUrl
                print createdate


                item = article_item(articleUrl, title, createdate)
                item.set_section_name(section_name)
                article_list.append(item)

        else:
            self.logger.error(u'没有获取到文章列表 ' + str(page_num) )

        return article_list


if __name__ == '__main__':
    shandong_spider = shandongSpider()
    shandong_spider.init_log('山东.log')
    shandong_spider.set_save_folder_path(globalconf.save_folder['shandong'])
    shandong_spider.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['shandong']
    shandong_spider.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in shandong_spider.section_key:
        shandong_spider.logger.info(u"获取栏目:" + section_item + ":" + shandong_spider.section_folder_map[section_item])
        for page_num in range(shandong_spider.page_number):
            article_list = shandong_spider.stripy_article_list(section_item, page_num)
            for item in article_list:
                shandong_spider.stripy_article_context(item)

