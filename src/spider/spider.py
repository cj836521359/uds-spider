#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chencharles'

from __init__ import *
import requests
import re
import sys
import os

from HTMLParser import *
import time
reload(sys)
sys.setdefaultencoding('utf-8')


class spiderBase:
    def __init__(self):
        self.url_base = ''
        self.page_number = 20
        self.section_key = []
        self.cur_page = 0
        self.folder_base = u'网省文件夹名'
        self.section_url_map = {}
        self.section_folder_map = {}
        self.section = None
        self.logger = None
        pass

    def init_log(self, log_name):
        '''
        初始化日志
        '''
        self.logger = log.init_log(log_name)

    def set_save_folder_path(self, save_folder):
        '''
        设置爬取保存目录
        '''
        self.save_folder = save_folder

    def set_limit_date_time(self, begin_date, end_date):
        '''
        设置爬取时间,例如20150101,20150202 ,由globalconf.py配置
        '''
        self.begin_date = time.strptime(begin_date, '%Y%m%d')
        self.end_date = time.strptime(end_date, '%Y%m%d')


    def is_in_date(self, str_date):
        '''
        判断要爬取的文件是否在指定实践内
        '''
        mydate = time.strptime(str_date, '%Y-%m-%d')
        if mydate >= self.begin_date and mydate <= self.end_date:
            return True
        else:
            return False



    def decode_data(self, encoding, str_data):
        '''
        用于解码判断,用chardet和request.encoding均有判断不准确情况.
        该函数后期可能去掉.
        '''
        if encoding == 'UTF-8':
            str_data = str_data.decode('UTF-8').strip()
        elif encoding == 'GBK' or encoding == 'gbk' or encoding == None:
            str_data = str_data.decode('gbk').strip()
        str_data = self.strip_tags(str_data)
        return str_data

    def init_session(self):
        self.session = requests.session()
        return self.session


    def init_mkdir_folder(self):
        '''
        创建文件夹
        '''
        for (k, v) in self.section_folder_map.items():
            if k in self.section_key:
                folder_name = self.save_folder + self.folder_base + "/" + v
                print folder_name
                if not os.path.isdir(folder_name):
                    os.makedirs(folder_name)

    def stripy_article_list(self, section_name, page_num):
        '''
        爬取文章列表,由子类实现
        '''
        article_list = []
        return article_list

    def strip_tags(self, html):
        '''
        清洗标签
        '''
        html = html.strip()
        html = html.strip("\n")
        result = []
        parser = HTMLParser()
        parser.handle_data = result.append
        parser.feed(html)
        parser.close()
        return ''.join(result).strip()

    def stripy_article_context(self, article_item):
        '''
        爬取文章内容并保存
        '''
        if self.is_in_date(article_item.public_time) == False:
            return

        self.logger.info(u"爬取文章")
        self.logger.info(article_item.article_url)
        self.logger.info(article_item.title)
        self.logger.info(article_item.public_time)
        title = article_item.title
        for rstr in common_utils.replace_str:
            if rstr in title:
               title = title.replace(rstr, "")
        title.strip()

        #获取扩展名
        ext = article_item.article_url.split("/")[-1]
        findExt = False
        for extType in common_utils.down_type:
            if extType in ext:
                findExt = True
                break

        file_name = self.folder_base + '/' \
                    + self.section_folder_map[article_item.section_name] + '/' \
                    + str(self.cur_page) + '_' + article_item.public_time + '_' + title

        if findExt == True:
            file_name = self.save_folder + file_name + ext
        else:
            file_name = self.save_folder + file_name + ".shtml"


        try:
            contentHtml = self.session.get(article_item.article_url, stream=True)

            if contentHtml.status_code == requests.codes.ok:
                self.logger.info( u'网页相应:返回成功')
                common_utils.write_to_file_with_stream(contentHtml.content, file_name)
            else:
                self.logger.error(u'下载失败!!!:' + file_name)
        except BaseException, e:
            self.logger.error(str(e))
            self.logger.error(article_item.article_url)
            self.logger.error(article_item.title)
            self.logger.error(u"获取网页数据失败")



    def set_section_list(self, section_lst):
        ll = list(set(self.section_key).intersection(set(section_lst)))
        self.section_key = ll
        return ll



if __name__ == '__main__':
    spider = spiderBase()
    spider.init_log('xxx')
