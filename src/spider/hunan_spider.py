# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
import demjson


class hunanSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = 'http://portal.hn.sgcc.com.cn/opencms/opencms'
        # self.logger = login.initLog('hunan.log')
        #self.page_number = 100
        print 'hunanSpider'
        self.session = self.init_session()
        self.folder_base = u'湖南'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            # 头版新闻
            'tbxw',
            # 公司要闻
            'gsyw',
            # 领导讲话
            'ldjh',
            # 基层动态
            'jcdt',
            # 综合新闻
            'zhxw',
            # 图片新闻
            'tpxw',
            # 本部新闻
            'bbxw',
            # 媒体报道
            'mtbd',
            # 国网要闻
            'gwyw',
            # 公告公示
            'gggs'
        ]



        self.section_url_map[self.section_key[0]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        self.section_url_map[self.section_key[1]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        self.section_url_map[self.section_key[2]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        self.section_url_map[self.section_key[3]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        self.section_url_map[self.section_key[4]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        self.section_url_map[self.section_key[5]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        self.section_url_map[self.section_key[6]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        self.section_url_map[self.section_key[7]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        self.section_url_map[self.section_key[8]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
        self.section_url_map[self.section_key[9]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'

        self.section_folder_map[self.section_key[0]] = u'头版新闻'
        self.section_folder_map[self.section_key[1]] = u'公司要闻'
        self.section_folder_map[self.section_key[2]] = u'领导讲话'
        self.section_folder_map[self.section_key[3]] = u'基层动态'
        self.section_folder_map[self.section_key[4]] = u'综合新闻'
        self.section_folder_map[self.section_key[5]] = u'图片新闻'
        self.section_folder_map[self.section_key[6]] = u'本部新闻'
        self.section_folder_map[self.section_key[7]] = u'媒体报道'
        self.section_folder_map[self.section_key[8]] = u'国网要闻'
        self.section_folder_map[self.section_key[9]] = u'公告公示'

        self.post_data_map[self.section_key[0]] = 'status=P&page=%s&id=00000491&child=true'
        self.post_data_map[self.section_key[1]] = 'status=P&page=%s&id=00000025&child=true'
        self.post_data_map[self.section_key[2]] = 'status=P&page=%s&id=00000027&child=true'
        self.post_data_map[self.section_key[3]] = 'status=P&page=%s&id=00000028&child=true'
        self.post_data_map[self.section_key[4]] = 'status=P&page=%s&id=00000029&child=true'
        self.post_data_map[self.section_key[5]] = 'status=P&page=%s&id=00000030&child=true'
        self.post_data_map[self.section_key[6]] = 'status=P&page=%s&id=00001490&child=true'
        self.post_data_map[self.section_key[7]] = 'status=P&page=%s&id=00001491&child=true'
        self.post_data_map[self.section_key[8]] = 'status=P&page=%s&id=00002041&child=true'
        self.post_data_map[self.section_key[9]] = 'status=P&page=%s&id=00000010&child=true'

        #头版新闻
        self.referer_map[self.section_key[0]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/sgcc/sgcc_topiccontentList.jsp?child=true&id=00000491'
        #公司要闻
        self.referer_map[self.section_key[1]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/sgcc/sgcc_topiccontentList.jsp?child=true&id=00000025'
        #领导讲话
        self.referer_map[self.section_key[2]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/sgcc/sgcc_topiccontentList.jsp?child=true&id=00000027'
        #基层动态
        self.referer_map[self.section_key[3]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/sgcc/sgcc_topiccontentList.jsp?child=true&id=00000028'
        #综合新闻
        self.referer_map[self.section_key[4]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/sgcc/sgcc_topiccontentList.jsp?child=true&id=00000029'
        ##湖南电力电视新闻
        #'jnddsxw':'status=P&page=%s&id=00000026&child=true',
        #图片新闻
        self.referer_map[self.section_key[5]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/sgcc/sgcc_topiccontentList.jsp?child=true&id=00000030'
        #本部新闻
        self.referer_map[self.section_key[6]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/sgcc/sgcc_topiccontentList.jsp?child=true&id=00001490'
        #媒体报道
        self.referer_map[self.section_key[7]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/sgcc/sgcc_topiccontentList.jsp?child=true&id=00001491'
        #国网要闻
        self.referer_map[self.section_key[8]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/sgcc/sgcc_topiccontentList.jsp?child=true&id=00002041'

        self.referer_map[self.section_key[9]] = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/sgcc/sgcc_topiccontentList.jsp?child=true&id=00000010'



    #爬取文章列表
    def stripy_article_list( self, section_name, page_num ):
        self.cur_page = page_num
        self.logger.info(self.cur_page)
        article_list = []
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            }
        data = self.post_data_map[section_name] %(self.cur_page)
        self.logger.info(data)
        #sys.exit(10)

        url = self.section_url_map[section_name]
        contentHtml = self.session.post(url, data=data, headers=headers)
        if contentHtml.encoding == 'gbk':
            contentHtml.encoding = 'gbk'
        else:
            contentHtml.encoding = 'utf-8'

        if contentHtml.status_code == 200:
            jsonDic = demjson.decode(contentHtml.text)

            for topiccontents in jsonDic['topiccontents']:
                title = topiccontents['title']
                filename = topiccontents['filename']
                url = topiccontents['url']
                createdate = time.strptime(topiccontents['createdate'],"%Y/%m/%d %H:%M:%S" )
                createdate = time.strftime('%Y-%m-%d',createdate)
                if url == "":
                    article_url = '%s%s' %(self.url_base, filename)
                else:
                    article_url = url


                item = article_item(article_url, title, createdate)
                item.set_section_name(section_name)
                article_list.append(item)

        else:
            self.logger.error(u'没有获取到文章列表 ' + str(page_num))
        return article_list



if __name__ == '__main__':
    hunan_spide = hunanSpider()
    hunan_spide.init_log(u'湖南.log')
    hunan_spide.set_save_folder_path(globalconf.save_folder['hunan'])
    hunan_spide.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['hunan']
    hunan_spide.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in hunan_spide.section_key:
        hunan_spide.logger.info(u"获取栏目:" + section_item + ":" + hunan_spide.section_folder_map[section_item])
        for page_num in range(hunan_spide.page_number):
            article_list = hunan_spide.stripy_article_list(section_item, page_num)
            for item in article_list:
                hunan_spide.stripy_article_context(item)

































            #头版新闻
            #status=P&page=1&id=00000491&child=true

            #公司要闻
            #status=P&page=1&id=00000025&child=true

            #领导讲话
            #status=P&page=1&id=00000027&child=true

            #基层动态
            #status=P&page=1&id=00000028&child=true

            #综合新闻
            #status=P&page=1&id=00000029&child=true

            #湖南电力电视新闻
            #status=P&page=1&id=00000026&child=true

            #图片新闻
            #status=P&page=1&id=00000030&child=true

            #本部新闻
            #status=P&page=1&id=00001490&child=true

            #媒体报道
            #status=P&page=1&id=00001491&child=true


            #国王要闻
            #status=P&page=1&id=00002041&child=true


            #sectionMap = {
            ##头版新闻
            #'tbxw':'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp',
            ##公司要闻
            #'gsyw':'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp',
            ##领导讲话
            #'ldjh':'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp',

            ##基层动态
            #'jcdt':'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp',

            ##综合新闻
            #'zhxw':'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp',

            ##湖南电力电视新闻
            #'jnddsxw':'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp',

            ##图片新闻
            #'tpxw':'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp',

            ##本部新闻
            #'bbxw':'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp',

            ##媒体报道
            #'mtbd':'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp',

            ##国网要闻
            #'gwyw':'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp',

            #}

            #folderMap = {

            ##头版新闻
            #'tbxw':u'头版新闻',
            ##公司要闻
            #'gsyw':u'公司要闻',
            ##领导讲话
            #'ldjh':u'领导讲话',

            ##基层动态
            #'jcdt':u'基层动态',

            ##综合新闻
            #'zhxw':u'综合新闻',

            ##湖南电力电视新闻
            #'jnddsxw':u'湖南电力电视新闻',

            ##图片新闻
            #'tpxw':u'图片新闻',

            ##本部新闻
            #'bbxw':u'本部新闻',

            ##媒体报道
            #'mtbd':u'媒体报道',


            ##国网要闻
            #'gwyw':u'国网要闻',

            #}


            #postDataMap = {
            ##头版新闻
            #'tbxw':'status=P&page=%s&id=00000491&child=true',
            ##公司要闻
            #'gsyw':'status=P&page=%s&id=00000025&child=true',
            ##领导讲话
            #'ldjh':'status=P&page=%s&id=00000027&child=true',

            ##基层动态
            #'jcdt':'status=P&page=%s&id=00000028&child=true',

            ##综合新闻
            #'zhxw':'status=P&page=%s&id=00000029&child=true',

            ##湖南电力电视新闻
            #'jnddsxw':'status=P&page=%s&id=00000026&child=true',

            ##图片新闻
            #'tpxw':'status=P&page=%s&id=00000030&child=true',

            ##本部新闻
            #'bbxw':'status=P&page=%s&id=00001490&child=true',

            ##媒体报道
            #'mtbd':'status=P&page=%s&id=00001491&child=true',


            ##国网要闻
            #'gwyw':'status=P&page=%s&id=00002041&child=true',
            #}

            #session = None

            #article_list = []

            #def init():
            #for (k,v) in folderMap.items():
            #folderName = folderbase.encode('gbk') + '/' + v.encode('gbk')
            #if not os.path.isdir(folderName):
            #os.makedirs(folderName)


            #def initSession():
            #session = requests.session()
            #return session

            #def stripy_article_list( sectionName, pageNum ):
            #global cur_page
            #cur_page = pageNum
            #logger.info(cur_page)
            #article_list = []
            #headers = {
            #'Content-Type': 'application/x-www-form-urlencoded',
            #}
            ##print sectionName
            ##print postDataMap
            ##sys.exit(1)
            #data = postDataMap[sectionName] %(cur_page)
            #logger.info(data)
            ##sys.exit(10)

            ##url = 'http://portal.hn.sgcc.com.cn/opencms/opencms/jsp/topicContentListJson.jsp'
            #url = sectionMap[ sectionName]
            #contentHtml = session.post( url ,data = data, headers=headers)
            #if contentHtml.encoding == 'gbk':
            #contentHtml.encoding = 'gbk'
            #else:
            #contentHtml.encoding = 'utf-8'
            ##common_utils.write_to_file(contentHtml.text,'abcdeg.txt')

            #if contentHtml.status_code == 200:
            ##print contentHtml.text
            #jsonDic = demjson.decode(contentHtml.text)

            #for topiccontents in jsonDic['topiccontents']:
            #title = topiccontents['title']
            #filename = topiccontents['filename']
            #url = topiccontents['url']
            ##print topiccontents['createdate']
            ##sys.exit(1)
            #createdate = time.strptime(topiccontents['createdate'],"%Y/%m/%d %H:%M:%S" )
            ##print createdate.strftime("%Y-%m-%d")
            #createdate = time.strftime('%Y-%m-%d',createdate)
            #if url == "":
            #article_url  = '%s%s' %(urlbase, filename )
            #else:
            #article_url = url
            ##print createdate
            ##sys.exit(1)


            #item = articleItem( article_url, title, createdate )
            ##item.setSectimeName( sectionName )

            ##item = articleItem( '','title' , 'public_time' )
            ##item.set_section_name( 'section_name' )
            #print item.public_time
            ##sys.exit(1)
            #if time.strptime(createdate,'%Y-%m-%d').tm_year == 2015:
            #article_list.append( (article_url, title) )

            #else:
            #logger.error(u'没有获取到文章列表 ' + str(pageNum) )
            ##sys.exit(1)
            ##print article_list[0][1]
            ##for (k,v) in article_list:
            ##print v
            ##sys.exit(1)

            #return article_list
            ##sys.exit(1)



            #def stripy_article_context( contentUrl, sectionName, title ):
            ##ext = os.path.splitext(contentUrl)[1]
            ##logger.info(title)

            #title=title.replace("\\","")
            #title=title.replace("/","")
            #title=title.replace("\"","")
            #title=title.replace(":","")
            #title=title.replace("*","")
            #title=title.replace("?","")
            #title=title.replace("","")
            #title=title.replace("<","")
            #title=title.replace(">","")
            #title=title.replace("|","")
            #title=title.replace("	","")
            #title.strip()
            ##replaceStr=["\\","/",":",":","*","?","\","<",">","|"]

            #logger.info(title)


            #fileName = folderbase + '/' + folderMap[sectionName] + '/' + str(cur_page) + '_' + title + '.shtml'
            #logger.info( contentUrl )
            #logger.info( fileName )
            #contentHtml = session.get(contentUrl)
            #print contentHtml.encoding
            ##===============================
            #if contentHtml.encoding == 'gbk':
            #contentHtml.encoding = 'gbk'
            #else:
            #contentHtml.encoding = 'utf-8'
            #if contentHtml.status_code == 200:
            #logger.info( u'返回成功')
            #common_utils.write_to_file( contentHtml.text, fileName )
            ##with open(fileName,'wb') as f:
            ##f.write( contentHtml.text )
            ##f.close()
            #else:
            #logger.error(u'下载失败!!!:' + fileName )





            #if __name__ == '__main__':
            #logger = login.initLog('hn.log')
            #init() #创建文件夹
            #session = initSession()


            ##for pageNum in range(15,16):
            #for k,v in sectionMap.items():
            #logger.info(u'获取栏目:' + k )
            #for pageNum in range(pageNumber):
            ##for pageNum in range(pageNumber):
            #article_list = stripy_article_list( k ,  pageNum )
            #for (url,title) in article_list:
            #stripy_article_context( url, k , title )

            ##国网要闻
            #'gwxw':u'国网要闻',
            ##公司要闻
            #'gsyw':u'公司要闻',
            ##本部新闻
            #'bbxw':u'本部新闻',
            ##媒体报道
            #'mtbd':u'媒体报道',
            ##基层动态 市基层
            #'jcdt_sjc':u'市基层',
            #'jcdt_xjc':u'省供电公司',
            ##视频在线
            #'spzx':u'视频在线'
            #for pageNum in range(pageNumber):
            ##for pageNum in range(8,9):
            #article_list = stripy_article_list( 'spzx' ,  pageNum )
            #for (url,title) in article_list:
            #stripy_article_context( url, 'spzx' , title )

