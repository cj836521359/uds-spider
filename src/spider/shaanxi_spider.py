# -*- coding: utf-8 -*-
#import spider
__author__ = 'chencharles'


from __init__ import *
from spider import *
import sys
import time
import chardet
import urllib

class shaanxiSpider(spiderBase):
    def __init__(self):
        spiderBase.__init__(self)
        self.url_base = ''
        print 'shaanxiSpider'
        self.session = self.init_session()
        self.folder_base = u'陕西'

        # section 文件夹
        self.section_folder_map = {}
        # 栏目对应的url
        self.section_url_map = {}
        self.post_data_map = {}
        self.referer_map = {}
        self.section_key = [
            # 公司要闻
            'gsyw',
            # 基层动态
            'jcdt',
            # 部门管理
            'bbgl',
            # 电网前期
            'dwqq',
            # 统计对标
            'tjdb',
            # 投资管理
            'tzgl',
            # 综合计划
            'zhjh',
            # 发展规划
            'fzgh',
            # 通知要求
            'tzyq',
            # 业务管控
            'ywgk',
            # 标准制度
            'zdbz',
            # 工作动态
            'gzdt',
            # 调度动态
            'dddt',
            # 智能电网动态
            'zndwdt',
            # 科研综合信息
            'kyzhxx',
            # 信息工作标准与制度
            'xxgzbzyzd',
            # 环保与工业卫生
            'hbygyws',
            # 信息化工作动态
            'xxjgzdt',
            # 信息化工作通报
            'xxhgztb',
            # 信息化知识园地与典型经验
            'xxhzsydydxjy',
            # 部门简介
            'dbjj',
            # 工作动态1
            'gzdt1',
            # 对标工作
            'dbgz',
            # 管理创新知识
            'glcxzs',
            # 管理创新成果
            'glcxcg',
            # 网站链接
            'wzlj',
            # 交易工作动态
            'jygzdt',
            # 每日工作安排
            'mrgzap',
            # 每周工作计划
            'mzgzap',
            # 规章制度文件
            'gzzdwj',
            # 月度工作计划
            'ydgzjh',
            # 季度交易信息
            'jdjyxx',
            # 组织建设
            'zzjs',
            # 厂务公开民主管理
            'cwgkmzgl',
            # 生产生活
            'scsj',
            # 宣教文体
            'xjwb',
            # 工会综合信息
            'gjzjxx',
            # 女工工作
            'nggz',
            # 公司要闻
            'gsyw',
            # 党的建设
            'ddjs',
            # 理论与宣传
            'llyxc',
            # 精神文明建设
            'jjwmjs',
            # 团青工作
            'tqgz',
            # 总揽
            'zl',
            # 动态
            'dt',
            # 论坛
            'lt',
            # 计划管理
            'jhgl',
            # 招标采购
            'zbcg',
            # 物资供应
            'wzgy',
            # 质量监督
            'zljd',
            # 学习资料
            'xxzl',
            # 工作动态2
            'gzdt2',
            # 同业对标
            'tydb',
            # 规章制度
            'gzzd',
            # 安全动态
            'aqdt',
            # 安全简报
            'aqjb',
            # 事故快报
            'sgkb',
            # 事故通报
            'sgtb',
            # 安全文件制度
            'aqwjzd',
            # 安全法律法规
            'aaflfg',
            # 领导讲话
            'ldjh',
            # 省公司规章制度
            'sgsgzzd',
            # 国网规章制度
            'gwgzzd',
            # 基建新闻
            'jjxw',
            # 项目管理
            'xmgl',
            # 技术管理
            'jjgl',
            # 安全管理
            'aqgl',
            # 质量管理
            'zlgl',
            # 造价管理
            'zjgl',
            # 综合管理
            'zhgl',
            ]




        #公司要闻
        self.section_url_map[self.section_key[0]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/8848E2A3E1ECCFBA4825781D0039CACD-s.xml'
        #基层动态
        self.section_url_map[self.section_key[1]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/614EC6E65DB71BCD4825781D003B0554-s.xml'
        #部门管理
        self.section_url_map[self.section_key[2]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/BC4350EBD1E37F2C4825779E003DAFF7-s.xml'
        #电网前期
        self.section_url_map[self.section_key[3]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/C1E3D2C03A016B7F4825779E003E9D93-s.xml'
        #统计对标
        self.section_url_map[self.section_key[4]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/B730175383AEAB574825779E003F17D6-s.xml'
        #投资管理
        self.section_url_map[self.section_key[5]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/6DA85D622C05B8A74825779E003F5A6B-s.xml'
        #综合计划
        self.section_url_map[self.section_key[6]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/8B332B53D5AD3EDB4825779E003FCD64-s.xml'
        #发展规划
        self.section_url_map[self.section_key[7]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/23083D9152DBC6214825779E003E6556-s.xml'
        #通知要求
        self.section_url_map[self.section_key[8]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/0DDE85929E5BAE1A48257B4B002DE961-s.xml'
        #业务管控
        self.section_url_map[self.section_key[9]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/7CD5AFED1A8F06C548257B4B002DF824-s.xml'
        #标准制度
        self.section_url_map[self.section_key[10]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/F677972C7B7EAF2348257B4B002E022E-s.xml'
        #工作动态
        self.section_url_map[self.section_key[11]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/30A771EDE9399B4C48257B4B002E0D1B-s.xml'
        #调度动态
        self.section_url_map[self.section_key[12]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/7275EE71FB1AE11A48257B660004BD9C-s.xml'
        #智能电网动态
        self.section_url_map[self.section_key[13]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/F7DA99DDEE7F2DDC48257C540004CB25-s.xml'
        #科研综合信息
        self.section_url_map[self.section_key[14]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/26B17D133193C0FD4825779E0043F51D-s.xml'
        #信息工作标准与制度
        self.section_url_map[self.section_key[15]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/B89265572532493848257AA1002931E4-s.xml'
        #环保与工业卫生
        self.section_url_map[self.section_key[16]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/312C7F66F8C3D4B34825779E0044BD3A-s.xml'
        #信息化工作动态
        self.section_url_map[self.section_key[17]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/E608D3661C84CD324825779E0044E5B4-s.xml'
        #信息化工作通报
        self.section_url_map[self.section_key[18]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/8FEC4516F95D0B014825779E00451E80-s.xml'
        #信息化知识园地与典型经验
        self.section_url_map[self.section_key[19]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/F88F5ED8A99E2FC24825779E00454559-s.xml'
        #部门简介
        self.section_url_map[self.section_key[20]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/BD02CBB8DA255B5448257CF3000C4B29-s.xml'
        #工作动态1
        self.section_url_map[self.section_key[21]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/7C67B7C375F6301C48257CBB003FBA28-s.xml'
        #对标工作
        self.section_url_map[self.section_key[22]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/53BA19D7D53672F148257DFC0008771C-s.xml'
        #管理创新知识
        self.section_url_map[self.section_key[23]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/B01B2C7388DE38DD48257CBB003FC431-s.xml'
        #管理创新成果
        self.section_url_map[self.section_key[24]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/CC630964EF65A0EE48257D2300291622-s.xml'
        #网站链接
        self.section_url_map[self.section_key[25]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/101DF96E0FA3FC1C48257CBB003FD18C-s.xml'
        #交易工作动态
        self.section_url_map[self.section_key[26]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/4623D37D0503C9E44825779E0046469F-s.xml'
        #每日工作安排
        self.section_url_map[self.section_key[27]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/A5A2F9A996B457864825779E00469324-s.xml'
        #每周工作计划
        self.section_url_map[self.section_key[28]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/0DA2E974809B20E44825779E0046B2E1-s.xml'
        #规章制度文件
        self.section_url_map[self.section_key[29]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/5FC139B9B56213134825779E0046DB1C-s.xml'
        #月度工作计划
        self.section_url_map[self.section_key[30]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/A5B1092FE5A3A0414825779E0046F936-s.xml'
        #季度交易信息
        self.section_url_map[self.section_key[31]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/131D08A25890541A4825779E0047132F-s.xml'
        #组织建设
        self.section_url_map[self.section_key[32]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/7223B3A389C6E4434825779E004649C3-s.xml'
        #厂务公开民主管理
        self.section_url_map[self.section_key[33]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/828D4D8C11E0F1D848257CE60006B1FC-s.xml'
        #生产生活
        self.section_url_map[self.section_key[34]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/2A7A26497AFFFD734825779F00088C26-s.xml'
        #宣教文体
        self.section_url_map[self.section_key[35]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/BBE845234C63A9D84825779F0007F80E-s.xml'
        #工会综合信息
        self.section_url_map[self.section_key[36]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/F1E185ACC04058E14825779E004685EF-s.xml'
        #女工工作
        self.section_url_map[self.section_key[37]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/9DDACDE1BFC5BF7E4825779E00463B30-s.xml'
        #公司要闻
        self.section_url_map[self.section_key[38]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/17530F8BD99B0E8A482577FC002DDB40-s.xml'
        #党的建设
        self.section_url_map[self.section_key[39]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/F62EA5D42FBF69E4482577FC002DE986-s.xml'
        #理论与宣传
        self.section_url_map[self.section_key[40]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/3A2BEC590318ACBF482577FC002DF939-s.xml'
        #精神文明建设
        self.section_url_map[self.section_key[41]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/0445F1052056C3CA482577FC002E034B-s.xml'
        #团青工作
        self.section_url_map[self.section_key[42]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/89830F8EFC9A8041482577FC002E0E0C-s.xml'
        #总揽
        self.section_url_map[self.section_key[43]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/4E4EEE28026E23CC482578E700298283-s.xml'
        #动态
        self.section_url_map[self.section_key[44]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/0629437EF6896857482578E7002A020E-s.xml'
        #论坛
        self.section_url_map[self.section_key[45]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/237A1597D3372C23482578E7002A131C-s.xml'
        #计划管理
        self.section_url_map[self.section_key[46]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/6D0CB4AA23B397E048257B1900297D5A-s.xml'
        #招标采购
        self.section_url_map[self.section_key[47]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/C796C4204FE5051648257B19002994D1-s.xml'
        #物资供应
        self.section_url_map[self.section_key[48]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/81E0BA796E4FF3FA48257B190029A1AD-s.xml'
        #质量监督
        self.section_url_map[self.section_key[49]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/9D52271EC2C30E6F48257B190029AD87-s.xml'
        #学习资料
        self.section_url_map[self.section_key[50]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/79E0A4691947B72F48257B190029BCDA-s.xml'
        #工作动态2
        self.section_url_map[self.section_key[51]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/91324F5A4A26F5DB482577ED001286F7-s.xml'
        #同业对标
        self.section_url_map[self.section_key[52]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/9A12B9DD6C5C640A48257B190029D5C4-s.xml'
        #规章制度
        self.section_url_map[self.section_key[53]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/C13D87C053A3C10748257B190029DD15-s.xml'
        #安全动态
        self.section_url_map[self.section_key[54]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/83E5438AA2C5B3BB4825779E004158D1-s.xml'
        #安全简报
        self.section_url_map[self.section_key[55]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/487DD771DC1088614825779E004299BC-s.xml'
        #事故快报
        self.section_url_map[self.section_key[56]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/84F83D194A9D2A004825779E0042700A-s.xml'
        #事故通报
        self.section_url_map[self.section_key[57]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/E2E1C16BEE44A5914825779E00425200-s.xml'
        #安全文件制度
        self.section_url_map[self.section_key[58]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/11158769A7DA2EB54825779E0042CE0E-s.xml'
        #安全法律法规
        self.section_url_map[self.section_key[59]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/BF89C41FDEA2E6F44825779E0042BCAA-s.xml'
        #领导讲话
        self.section_url_map[self.section_key[60]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/387DEE3AD7B0ACF7482577E4002AB523-s.xml'
        #省公司规章制度
        self.section_url_map[self.section_key[61]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/0AE98811F78F1902482577E4002ADC4B-s.xml'
        #国网规章制度
        self.section_url_map[self.section_key[62]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/F65689A675308F0448257855002AE743-s.xml'
        #基建新闻
        self.section_url_map[self.section_key[63]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/A0AA0F98E7FDED15482577E4002B056D-s.xml'
        #项目管理
        self.section_url_map[self.section_key[64]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/DE7DE1D114BB2B40482577E4002B14A5-s.xml'
        #技术管理
        self.section_url_map[self.section_key[65]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/E84415C91CB83315482577E4002B23E1-s.xml'
        #安全管理
        self.section_url_map[self.section_key[66]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/6475FEDDE7AA6204482577E4002B3103-s.xml'
        #质量管理
        self.section_url_map[self.section_key[67]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/9A3B5937B0644556482577E4002B3CBE-s.xml'
        #造价管理
        self.section_url_map[self.section_key[68]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/FA41677CDD5CEDEA482577E4002B4BFB-s.xml'
        #综合管理
        self.section_url_map[self.section_key[69]] = 'http://portal.sn.sgcc.com.cn/WEBFFF/view/EA2E127F30D9F9B1482577E4002B6C0C-s.xml'






        #公司要闻
        self.section_folder_map[self.section_key[0]] = u'公司要闻'
        #基层动态
        self.section_folder_map[self.section_key[1]] = u'基层动态'
        #部门管理
        self.section_folder_map[self.section_key[2]] = u'部门管理'
        #电网前期
        self.section_folder_map[self.section_key[3]] = u'电网前期'
        #统计对标
        self.section_folder_map[self.section_key[4]] = u'统计对标'
        #投资管理
        self.section_folder_map[self.section_key[5]] = u'投资管理'
        #综合计划
        self.section_folder_map[self.section_key[6]] = u'综合计划'
        #发展规划
        self.section_folder_map[self.section_key[7]] = u'发展规划'
        #通知要求
        self.section_folder_map[self.section_key[8]] = u'通知要求'
        #业务管控
        self.section_folder_map[self.section_key[9]] = u'业务管控'
        #标准制度
        self.section_folder_map[self.section_key[10]] = u'标准制度'
        #工作动态
        self.section_folder_map[self.section_key[11]] = u'工作动态'
        #调度动态
        self.section_folder_map[self.section_key[12]] = u'调度动态'
        #智能电网动态
        self.section_folder_map[self.section_key[13]] = u'智能电网动态'
        #科研综合信息
        self.section_folder_map[self.section_key[14]] = u'科研综合信息'
        #信息工作标准与制度
        self.section_folder_map[self.section_key[15]] = u'信息工作标准与制度'
        #环保与工业卫生
        self.section_folder_map[self.section_key[16]] = u'环保与工业卫生'
        #信息化工作动态
        self.section_folder_map[self.section_key[17]] = u'信息化工作动态'
        #信息化工作通报
        self.section_folder_map[self.section_key[18]] = u'信息化工作通报'
        #信息化知识园地与典型经验
        self.section_folder_map[self.section_key[19]] = u'信息化知识园地与典型经验'
        #部门简介
        self.section_folder_map[self.section_key[20]] = u'部门简介'
        #工作动态1
        self.section_folder_map[self.section_key[21]] = u'工作动态1'
        #对标工作
        self.section_folder_map[self.section_key[22]] = u'对标工作'
        #管理创新知识
        self.section_folder_map[self.section_key[23]] = u'管理创新知识'
        #管理创新成果
        self.section_folder_map[self.section_key[24]] = u'管理创新成果'
        #网站链接
        self.section_folder_map[self.section_key[25]] = u'网站链接'
        #交易工作动态
        self.section_folder_map[self.section_key[26]] = u'交易工作动态'
        #每日工作安排
        self.section_folder_map[self.section_key[27]] = u'每日工作安排'
        #每周工作计划
        self.section_folder_map[self.section_key[28]] = u'每周工作计划'
        #规章制度文件
        self.section_folder_map[self.section_key[29]] = u'规章制度文件'
        #月度工作计划
        self.section_folder_map[self.section_key[30]] = u'月度工作计划'
        #季度交易信息
        self.section_folder_map[self.section_key[31]] = u'季度交易信息'
        #组织建设
        self.section_folder_map[self.section_key[32]] = u'组织建设'
        #厂务公开民主管理
        self.section_folder_map[self.section_key[33]] = u'厂务公开民主管理'
        #生产生活
        self.section_folder_map[self.section_key[34]] = u'生产生活'
        #宣教文体
        self.section_folder_map[self.section_key[35]] = u'宣教文体'
        #工会综合信息
        self.section_folder_map[self.section_key[36]] = u'工会综合信息'
        #女工工作
        self.section_folder_map[self.section_key[37]] = u'女工工作'
        #公司要闻
        self.section_folder_map[self.section_key[38]] = u'公司要闻'
        #党的建设
        self.section_folder_map[self.section_key[39]] = u'党的建设'
        #理论与宣传
        self.section_folder_map[self.section_key[40]] = u'理论与宣传'
        #精神文明建设
        self.section_folder_map[self.section_key[41]] = u'精神文明建设'
        #团青工作
        self.section_folder_map[self.section_key[42]] = u'团青工作'
        #总揽
        self.section_folder_map[self.section_key[43]] = u'总揽'
        #动态
        self.section_folder_map[self.section_key[44]] = u'动态'
        #论坛
        self.section_folder_map[self.section_key[45]] = u'论坛'
        #计划管理
        self.section_folder_map[self.section_key[46]] = u'计划管理'
        #招标采购
        self.section_folder_map[self.section_key[47]] = u'招标采购'
        #物资供应
        self.section_folder_map[self.section_key[48]] = u'物资供应'
        #质量监督
        self.section_folder_map[self.section_key[49]] = u'质量监督'
        #学习资料
        self.section_folder_map[self.section_key[50]] = u'学习资料'
        #工作动态2
        self.section_folder_map[self.section_key[51]] = u'工作动态2'
        #同业对标
        self.section_folder_map[self.section_key[52]] = u'同业对标'
        #规章制度
        self.section_folder_map[self.section_key[53]] = u'规章制度'
        #安全动态
        self.section_folder_map[self.section_key[54]] = u'安全动态'
        #安全简报
        self.section_folder_map[self.section_key[55]] = u'安全简报'
        #事故快报
        self.section_folder_map[self.section_key[56]] = u'事故快报'
        #事故通报
        self.section_folder_map[self.section_key[57]] = u'事故通报'
        #安全文件制度
        self.section_folder_map[self.section_key[58]] = u'安全文件制度'
        #安全法律法规
        self.section_folder_map[self.section_key[59]] = u'安全法律法规'
        #领导讲话
        self.section_folder_map[self.section_key[60]] = u'领导讲话'
        #省公司规章制度
        self.section_folder_map[self.section_key[61]] = u'省公司规章制度'
        #国网规章制度
        self.section_folder_map[self.section_key[62]] = u'国网规章制度'
        #基建新闻
        self.section_folder_map[self.section_key[63]] = u'基建新闻'
        #项目管理
        self.section_folder_map[self.section_key[64]] = u'项目管理'
        #技术管理
        self.section_folder_map[self.section_key[65]] = u'技术管理'
        #安全管理
        self.section_folder_map[self.section_key[66]] = u'安全管理'
        #质量管理
        self.section_folder_map[self.section_key[67]] = u'质量管理'
        #造价管理
        self.section_folder_map[self.section_key[68]] = u'造价管理'
        #综合管理
        self.section_folder_map[self.section_key[69]] = u'综合管理'


        # self.init_mkdir_folder()



    #爬取文章列表
    def stripy_article_list(self, section_name, page_num):
        try:
            self.cur_page = page_num
            article_list = []
            if page_num == 0:
                url = self.section_url_map[section_name]
            else:
                url = self.section_url_map[section_name][0:-6] + str(self.cur_page) + '.html'
            print url

            contentHtml = self.session.get(url, stream=True)
            encoding = chardet.detect(contentHtml.content)['encoding']

            if contentHtml.status_code == requests.codes.ok:
                pattern = r'<item><news_id>.*?</news_id><title><!\[CDATA\[(.*?)\]\].*?</title><link>(.*?)</link>.*?<pubDate>(\d{4}-\d{2}-\d{2}).*?</pubDate>'
                for mtFind in re.finditer(pattern, contentHtml.content, re.S):
                    if mtFind.groups()[0][0:4] == "http":
                        article_url = mtFind.groups()[0]
                    else:
                        proto,rest = urllib.splittype( self.section_url_map[section_name])
                        article_url = proto + "://" + urllib.splithost(rest)[0] + "/" + mtFind.groups()[1][1:]


                    public_time = self.strip_tags(mtFind.groups()[2])
                    title = mtFind.groups()[0].decode(encoding)

                    print public_time
                    ##print repr(title)
                    print title
                    print article_url

                    item = article_item(article_url, title, public_time)
                    item.set_section_name(section_name)
                    article_list.append(item)
            else:
                self.logger.error(u'没有获取到文章列表 ' + str(page_num))
        except:
            self.logger.error(u"获取网页失败" + url)
        finally:
            return article_list






if __name__ == '__main__':
    shaanxi_spide = shaanxiSpider()
    shaanxi_spide.init_log(u'陕西.log')
    shaanxi_spide.set_save_folder_path(globalconf.save_folder['shaanxi'])
    shaanxi_spide.init_mkdir_folder()
    str_limit_date = globalconf.spider_limit_date_time['shaanxi']
    shaanxi_spide.set_limit_date_time(str_limit_date[0:8], str_limit_date[9:])
    for section_item in shaanxi_spide.section_key:
        shaanxi_spide.logger.info(u"获取栏目:" + section_item + ":" + shaanxi_spide.section_folder_map[section_item])
        for page_num in range(shaanxi_spide.page_number):
            article_list = shaanxi_spide.stripy_article_list(section_item, page_num)
            for item in article_list:
                shaanxi_spide.stripy_article_context(item)













