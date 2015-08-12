# -*- coding: utf-8 -*-

__author__ = "zhy"

import os
import codecs
import sys
import re
import icu
from HTMLParser import HTMLParser
from pyquery import PyQuery as pq

# csv文件保存目录
#csv_path = u'/Users/zhy/works/20.亿榕/0.0.公司项目/11非结构化数据分析与利用/30.数据/门户数据/CSV'
csv_path = u'/Users/tina/workspace/NLP/20150811/CSV_TITLE'

def paser_all(path):
    for area_path in os.listdir(path):
        area_path = os.path.join(path, area_path)
        if os.path.isdir(area_path):
            paser_area(area_path)


def paser_area(area_path):
    for mou_path in os.listdir(area_path):
        mou_path = os.path.join(area_path, mou_path)
        if os.path.isdir(mou_path):
            paser_mou(mou_path)


def paser_mou(mou_path):
    area_path, mou_name = os.path.split(mou_path)
    area_name = os.path.basename(area_path)
    with codecs.open(os.path.join(csv_path, area_name+'_'+mou_name+'.csv'), 'w', 'utf-8') as f:
        for htm in os.listdir(mou_path):
            htm_file = os.path.join(mou_path, htm)
            if os.path.isfile(htm_file):
                row_data = ''
                #row_data = paser_htm(htm_file, area_name, mou_name)
                area,mou,title_name,date_name,html_content = paser_htm(htm_file, area_name, mou_name)
                if area == '':
                    continue

                keylst = [u"负荷",
                        u"用电量",
                        u"新高"
                        ]

                keys = ""
                bhit = False
                for keyitem in keylst:
                    #if re.search(keyitem,html_content):
                    if re.search(keyitem,title_name):
                        keys = keys + keyitem + ","
                        bhit = True
                    else:
                        keys = keys + "" + ","

                keys = keys[0:-1]
                if bhit == False:
                    continue


                #print keys
                #sys.exit(1)
                row_data = area + ',' + mou + ',' + title_name + ',' + date_name + ',' + keys + ',' + html_content
                row_data = re.sub(r'[\n\r]+', '', row_data)
                #for key in lsFind:
                    #row_data = area + ',' + mou + ',' + title_name + ',' + date_name + ',' + key + ',' + html_content
                    #row_data = re.sub(r'[\n\r]+', '', row_data)
                if not row_data:
                    continue
                #if not re.match(r'^[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+$', row_data):
                    #print '============================================================'
                    #print 'Has error:',htm_file
                    #print row_data
                #else:
                f.write(row_data)
                f.write('\n')


def paser_htm(htm_path, area, mou):
    #print htm_path
    file_name = os.path.splitext(os.path.basename(htm_path))[0]
    m = re.match(r'^[\d_-]+([\S\s]+)$', file_name)
    if(m):
        title_name = m.group(1)
        title_name = replace_dou(title_name)
    else:
        return '','','','',''
    try:
        title_name = pq(title_name).html()
    except Exception:
        print u'标题转换错误：', title_name
    # 先取得文件的正确编码
    with open(htm_path, 'r') as cf:
        coding = icu.CharsetDetector(cf.read()).detect().getName()
    # 用取得的文件编码打开文件，读取内容
    with codecs.open( htm_path, 'r', coding) as f:
        try:
            html_text = f.read()
        except Exception:
            return '','','','',''
        date_name = get_date(file_name, html_text)
        content = get_content(html_text)
        content = replace_dou(content)
    #print area,mou,title_name,date_name
    return area,mou,title_name,date_name,content
    row_data = area + ',' + mou + ',' + title_name + ',' + date_name + ',' + content
    row_data = re.sub(r'[\n\r]+', '', row_data)
    return row_data

def get_date(file_name, html_text):
    r = re.match(r'^\d+_(\d{4}-\d{2}-\d{2})', file_name)
    if r:
        return r.group(1)
    else:
        r = re.search(r'([^\x00-\xff]{4,5})[\]\s]*(\d{2,4}-\d{2}-\d{2})', html_text)
        if r:
            date_name = r.group(2)
        else:
            date_name = u'空'
        return date_name


def get_content(html_text):
    # 取网页内容块的样式名称
    # .cmscontent
    # .content-content 信通
    # #articalcontent 甘肃
    # .lmxx_b2014 冀北
    # .style4 天津
    # .news_content 河北
    # .detailTabDetail 上海
    # .fontme 安徽
    # .bt_content 江苏
    # .a_showzw 重庆
    # #artibody 西藏、山西
    # .c_content 河南
    # .12_black 辽宁
    # .thetext 内蒙古
    # .con_article_body_content 青海
    # .Custom_UnionStyle 浙江
    # .page_text .content 北京
    # .nr:last 黑龙江
    # .content_cms 湖南
    # .caption_info2 山东
    # .contentMain 陕西
    cls = ['.cmscontent', '.content-content', '#articlecontent',
            '.lmxx_b2014', '.style4', '.news_content', '.detailTabDetail',
            '.fontme', '.bt_content', '.a_showzw', '#artibody', '.c_content',
            '.thetext', '.con_article_body_content', '.Custom_UnionStyle',
            '.page_text', '.content', '.nr:last', '.content_cms', '.caption_info2',
            '.newsmain']
    try:
        d = pq(html_text)
    except Exception:
        print u'pyquery解析网页内容错误，请检查网页内容'
        return ""
    d('style').remove()
    d('script').remove()
    content = ''
    # for p in d('p'):
        # if p:
            # content += strip_tags(d(p).html())
    for cl in cls:
        try:
            if d(cl):
                content = strip_tags(d(cl).html())
                break
        except Exception:
            print u'获取内容错误：', cl
    return content

def convert_encoding(data, new_coding='utf-8'):
    """
    自动判断编码，然后将数据转换为指定的编码。默认utf-8
    """
    coding = icu.CharsetDetector(data).detect().getName()
    if new_coding.upper() != coding.upper():
        data = unicode(data, coding).encode(new_coding)
    return data

def replace_dou(string):
    dou = re.compile(',')
    new_string = dou.sub(u'，', string)
    new_string = new_string.strip()
    new_string = new_string.strip('\n')
    new_string = new_string.strip('\r')
    return new_string


#用了HTMLParser，有更简单的方式吗
def strip_tags(html):
    """
    Python中过滤HTML标签的函数
    """
    if html is None:
        return ''
    html = html.strip()
    html = html.strip("\n")
    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(html)
    parser.close()
    return ''.join(result)

if __name__ == '__main__':
    #pa = u'/Users/tina/workspace/NLP/20150811/安徽/'
    #pa = u'/Users/tina/workspace/NLP/20150811/北京/'
    #pa = u'/Users/tina/workspace/NLP/20150811/重庆/'
    #pa = u'/Users/tina/workspace/NLP/20150811/福建/'
    #pa = u'/Users/tina/workspace/NLP/20150811/甘肃/'
    #pa = u'/Users/tina/workspace/NLP/20150811/河北/'
    #pa = u'/Users/tina/workspace/NLP/20150811/河南/'
    #pa = u'/Users/tina/workspace/NLP/20150811/黑龙江/'
    #pa = u'/Users/tina/workspace/NLP/20150811/湖北/'
    #pa = u'/Users/tina/workspace/NLP/20150811/湖南/'
    #pa = u'/Users/tina/workspace/NLP/20150811/吉林/'
    mylst=[
            #u'/Users/tina/workspace/NLP/20150811/上海/',
            #u'/Users/tina/workspace/NLP/20150811/信通/',
            #u'/Users/tina/workspace/NLP/20150811/冀北/',
            #u'/Users/tina/workspace/NLP/20150811/北京/',
            #u'/Users/tina/workspace/NLP/20150811/吉林/',
            #u'/Users/tina/workspace/NLP/20150811/四川/',
            #u'/Users/tina/workspace/NLP/20150811/天津/',
            #u'/Users/tina/workspace/NLP/20150811/宁夏/',
            #u'/Users/tina/workspace/NLP/20150811/安徽/',
            #u'/Users/tina/workspace/NLP/20150811/客服/',
            #u'/Users/tina/workspace/NLP/20150811/山东/',
            #u'/Users/tina/workspace/NLP/20150811/山西/',
            #u'/Users/tina/workspace/NLP/20150811/新疆/',
            #u'/Users/tina/workspace/NLP/20150811/江苏/',
            #u'/Users/tina/workspace/NLP/20150811/河北/',
            #u'/Users/tina/workspace/NLP/20150811/河南/',
            #u'/Users/tina/workspace/NLP/20150811/湖北/',
            #u'/Users/tina/workspace/NLP/20150811/湖南/',
            #u'/Users/tina/workspace/NLP/20150811/甘肃/',
            #u'/Users/tina/workspace/NLP/20150811/福建/',
            #u'/Users/tina/workspace/NLP/20150811/西藏/',
            #u'/Users/tina/workspace/NLP/20150811/浙江/',
            #u'/Users/tina/workspace/NLP/20150811/重庆/',
            #u'/Users/tina/workspace/NLP/20150811/陕西/',
            #u'/Users/tina/workspace/NLP/20150811/青海/',
            #u'/Users/tina/workspace/NLP/20150811/内蒙古/',
            #u'/Users/tina/workspace/NLP/20150811/黑龙江/',

            u'/Users/tina/workspace/NLP/20150811/辽宁/',
            u'/Users/tina/workspace/NLP/20150811/江西/',
            ]
    for i in mylst:
        print i
        lis = paser_area(i)
    # print lis

    # ph = paser_htm(u'/Users/zhy/works/20.亿榕/0.0.公司项目/11非结构化数据分析与利用/30.数据/门户数据/原始数据/辽宁/基层动态/7_2015-04-14_葫芦岛公司：五个“注重”强化安全生产工作.shtml', u'辽宁', u'测试')
    # print ph
