# -*- coding: utf-8 -*-
__author__ = 'chencharles'


import demjson

str = """
{
    "save_path": "../Data/",
    "limit_date":"20150405-20150422",
    "provinces": [
        {
            "key": "anhui",
            "name":"安徽",
            "logname":"../Log/安徽.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gsxw","gsxw":{"spider":true,"name":"公司新闻"}},
                {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
                {"id":"bbdt","bbdt":{"spider":true,"name":"本部动态"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
                {"id":"zhzx","zhzx":{"spider":true,"name":"综合资讯"}},
                {"id":"mtjj","mtjj":{"spider":true,"name":"媒体聚焦"}}
            ]
        },
        {
            "key": "beijing",
            "name":"北京",
            "logname":"../Log/北京.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
                {"id":"zxtz","zxtz":{"spider":true,"name":"最新通知"}}
            ]
        },
        {
            "key": "chongqing",
            "name":"重庆",
            "logname":"../Log/重庆.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"gwyw","gwyw":{"spider":true,"name":"国网要闻"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
                {"id":"czxkjcx","czxkjcx":{"spider":true,"name":"群众性科技创新"}}
            ]
        },
        {
            "key": "fujian",
            "name":"福建",
            "logname":"../Log/福建.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gwyw","gwyw":{"spider":true,"name":"国网要闻"}},
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
                {"id":"zxtz","zxtz":{"spider":true,"name":"最新通知"}}
            ]
        },
        {
            "key": "gansu",
            "name":"甘肃",
            "logname":"../Log/甘肃.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gwdt","gwdt":{"spider":true,"name":"国网动态"}},
                {"id":"gsxw","gsxw":{"spider":true,"name":"公司新闻"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
                {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}}
            ]
        },
        {
            "key": "hebei",
            "name":"河北",
            "logname":"../Log/河北.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gwsd","gwsd":{"spider":true,"name":"国网速递"}},
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"gsxw","gsxw":{"spider":true,"name":"公司新闻"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
                {"id":"tpxw","tpxw":{"spider":true,"name":"图片新闻"}}
            ]
        },
        {
            "key": "heilongjiang",
            "name":"黑龙江",
            "logname":"../Log/黑龙江.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
                {"id":"kjxx_gzdt","kjxx_gzdt":{"spider":true,"name":"科技信息-工作动态"}},
                {"id":"kjxx_gzcg","kjxx_gzcg":{"spider":true,"name":"科技信息-工作成果"}},
                {"id":"yxfw_zcfg","yxfw_zcfg":{"spider":true,"name":"营销服务-政策法规"}},
                {"id":"yxfw_gzdt","yxfw_gzdt":{"spider":true,"name":"营销服务-工作动态"}},
                {"id":"ncdl_ndxx","ncdl_ndxx":{"spider":true,"name":"农村电力-农电信息"}},
                {"id":"ncdl_nwfz","ncdl_nwfz":{"spider":true,"name":"农村电力-农网发展"}},
                {"id":"ncdl_ndfw","ncdl_ndfw":{"spider":true,"name":"农村电力-农电服务"}},
                {"id":"zggz_gzbs","zggz_gzbs":{"spider":true,"name":"政工工作-工作部署"}},
                {"id":"zggz_gzbs","zggz_gzbs":{"spider":true,"name":"政工工作-工作部署"}},
                {"id":"zggz_zdgf","zggz_zdgf":{"spider":true,"name":"政工工作-制度规范"}},
                {"id":"zggz_zcsj","zggz_zcsj":{"spider":true,"name":"政工工作-基层实践"}},
                {"id":"dwjs_gcdt","dwjs_gcdt":{"spider":true,"name":"电网建设-工程动态"}},
                {"id":"dwjs_bzgf","dwjs_bzgf":{"spider":true,"name":"电网建设-标准规范"}},
                {"id":"dwjs_aqzl","dwjs_aqzl":{"spider":true,"name":"电网建设-安全质量"}},
                {"id":"dwjs_hdzl","dwjs_hdzl":{"spider":true,"name":"电网建设-基建安全质量年活动专栏"}},
                {"id":"aqbw","aqbw":{"spider":true,"name":"安全保卫"}},
                {"id":"aqxx","aqxx":{"spider":true,"name":"安全信息"}}
            ]
        },
        {
        "key": "henan",
        "name":"河南",
        "logname":"../Log/河南.log",
		"need_spider":false,
        "save_path":"../Data/",
        "limit_date":"20150405-20150422",
        "sections": [
            {"id":"gsxw","gsxw":{"spider":true,"name":"公司新闻"}},
            {"id":"jcdt_sgs","jcdt_sgs":{"spider":true,"name":"市公司动态"}},
            {"id":"jcdt_xgs","jcdt_xgs":{"spider":true,"name":"县公司动态"}},
            {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}}
            ]
        },
        {
        "key": "hubei",
        "name":"湖北",
        "logname":"../Log/湖北.log",
		"need_spider":false,
        "save_path":"../Data/",
        "limit_date":"20150405-20150422",
        "sections": [
            {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
            {"id":"ldjh","ldjh":{"spider":true,"name":"领导讲话"}},
            {"id":"bbdt","bbdt":{"spider":true,"name":"本部动态"}},
            {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
            {"id":"gzjl","gzjl":{"spider":true,"name":"工作交流"}},
            {"id":"gzyj","gzyj":{"spider":true,"name":"工作研究"}},
            {"id":"yxfc","yxfc":{"spider":true,"name":"一线风采"}}
            ]
        },
        {
            "key": "hunan",
            "name":"湖南",
            "logname":"../Log/湖南.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"tbxw","tbxw":{"spider":true,"name":"头版新闻"}},
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"ldjh","ldjh":{"spider":true,"name":"领导讲话"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
                {"id":"zhxw","zhxw":{"spider":true,"name":"综合新闻"}},
                {"id":"tpxw","tpxw":{"spider":true,"name":"图片新闻"}},
                {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
                {"id":"gwyw","gwyw":{"spider":true,"name":"国网要闻"}},
                {"id":"gggs","gggs":{"spider":true,"name":"公告公示"}}

                ]
        },
        {
        "key": "jiangsu",
        "name":"江苏",
        "logname":"../Log/江苏.log",
		"need_spider":false,
        "save_path":"../Data/",
        "limit_date":"20150405-20150422",
        "sections": [
            {"id":"gwyw","gwyw":{"spider":true,"name":"国网要闻"}},
            {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
            {"id":"bbdt","bbdt":{"spider":true,"name":"本部动态"}},
            {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
            {"id":"jbsp","jbsp":{"spider":true,"name":"广角镜"}},
            {"id":"jcljs","jcljs":{"spider":true,"name":"基层链接市"}},
            {"id":"jcljx","jcljx":{"spider":true,"name":"基层链接县"}}
            ]
        },
         {
            "key": "jiangxi",
            "name":"江西",
            "logname":"../Log/江西.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gwxw","gwxw":{"spider":true,"name":"国网要闻"}},
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
                {"id":"ldjh","ldjh":{"spider":true,"name":"领导讲话"}}
                ]
        },
        {
            "key": "jibei",
            "name":"冀北",
            "logname":"../Log/冀北.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
                {"id":"jcdt_dsgs","jcdt_dsgs":{"spider":true,"name":"基层动态-地市公司"}},
                {"id":"jcdt_sgdgs","jcdt_sgdgs":{"spider":true,"name":"基层动态-县供电公司"}},
                {"id":"jbsp","jbsp":{"spider":true,"name":"冀北时评 "}},
                {"id":"rdzt","rdzt":{"spider":true,"name":"热点专题"}}

                ]
        },
        {
            "key": "jilin",
            "name":"吉林",
            "logname":"../Log/吉林.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
               {"id":"gwxw","gwxw":{"spider":true,"name":"国网要闻"}},
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"bbxw","bbxw":{"spider":true,"name":"本部动态"}},
                {"id":"mtfy","mtfy":{"spider":true,"name":"媒体反应"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
                {"id":"zytz","zytz":{"spider":true,"name":"最新通知"}}
                ]
        },
        {
            "key": "kefu",
            "name":"客服",
            "logname":"../Log/客服.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"zxyw","zxyw":{"spider":true,"name":"中心要闻"}},
                {"id":"zytz","zytz":{"spider":true,"name":"媒体报道"}},
                {"id":"gzdt","gzdt":{"spider":true,"name":"工作动态 中心本部"}},
                {"id":"fzxdt","fzxdt":{"spider":true,"name":"南北分中心"}},
                {"id":"yxfc","yxfc":{"spider":true,"name":"一线风采"}},
                {"id":"zgyy","zgyy":{"spider":true,"name":"职工艺苑"}}

                ]
        },
        {
        "key": "liaoning",
        "name":"辽宁",
        "logname":"../Log/辽宁.log",
		"need_spider":false,
        "save_path":"../Data/",
        "limit_date":"20150405-20150422",
        "sections": [
            {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
            {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
            {"id":"hytz","hytz":{"spider":true,"name":"会议通知"}},
            {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
            {"id":"qyxx","qyxx":{"spider":true,"name":"企业信息"}}

            ]
        },
        {
        "key": "neimenggu",
        "name":"内蒙古",
        "logname":"../Log/内蒙古.log",
		"need_spider":false,
        "save_path":"../Data/",
        "limit_date":"20150405-20150422",
        "sections": [

            {"id":"zytz","zytz":{"spider":true,"name":"重要通知"}},
            {"id":"ttxw","ttxw":{"spider":true,"name":"头条新闻"}},
            {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
            {"id":"jjxx","jjxx":{"spider":true,"name":"基层信息"}},
            {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
            {"id":"ldjh","ldjh":{"spider":true,"name":"领导讲话"}},
            {"id":"hyxx","hyxx":{"spider":true,"name":"行业信息"}},


            ]
        },
         {
            "key": "ningxia",
            "name":"宁夏",
            "logname":"../Log/宁夏.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gwyw","gwyw":{"spider":true,"name":"国网要闻"}},
                {"id":"gsxw","gsxw":{"spider":true,"name":"公司新闻"}},
                {"id":"txbd","txbd":{"spider":true,"name":"通讯报道"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
                {"id":"xyxw_gwdt","xyxw_gwdt":{"spider":true,"name":"行业新闻"}},
                {"id":"zxxx","zxxx":{"spider":true,"name":"综合信息"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}}
                ]
        },
        {
            "key": "qinghai",
            "name":"青海",
            "logname":"../Log/青海.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"ttxw","ttxw":{"spider":true,"name":"头条新闻"}},
                {"id":"qdkx","qdkx":{"spider":true,"name":"青电快讯"}},
                {"id":"mtjj","mtjj":{"spider":true,"name":"媒体聚焦"}},
                {"id":"tpxw","tpxw":{"spider":true,"name":"图片新闻"}},
                {"id":"gg","gg":{"spider":true,"name":"公告"}}
                ]
        },
        {
        "key": "shaanxi",
        "name":"陕西",
        "logname":"../Log/陕西.log",
		"need_spider":false,
        "save_path":"../Data/",
        "limit_date":"20150405-20150422",
        "sections": [
            {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
            {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
            {"id":"bbgl","bbgl":{"spider":true,"name":"部门管理"}},
            {"id":"dwqq","dwqq":{"spider":true,"name":"电网前期"}},
            {"id":"tjdb","tjdb":{"spider":true,"name":"统计对标"}},
            {"id":"tzgl","tzgl":{"spider":true,"name":"投资管理"}},
            {"id":"zhjh","zhjh":{"spider":true,"name":"综合计划"}},
            {"id":"fzgh","fzgh":{"spider":true,"name":"发展规划"}},
            {"id":"tzyq","tzyq":{"spider":true,"name":"通知要求"}},
            {"id":"ywgk","ywgk":{"spider":true,"name":"业务管控"}},
            {"id":"zdbz","zdbz":{"spider":true,"name":"标准制度"}},
            {"id":"gzdt","gzdt":{"spider":true,"name":"工作动态"}},
            {"id":"dddt","dddt":{"spider":true,"name":"调度动态"}},
            {"id":"zndwdt","zndwdt":{"spider":true,"name":"智能电网动态"}},
            {"id":"kyzhxx","kyzhxx":{"spider":true,"name":"科研综合信息"}},
            {"id":"xxgzbzyzd","xxgzbzyzd":{"spider":true,"name":"信息工作标准与制度"}},
            {"id":"hbygyws","hbygyws":{"spider":true,"name":"环保与工业卫生"}},
            {"id":"xxjgzdt","xxjgzdt":{"spider":true,"name":"信息化工作动态"}},
            {"id":"xxhgztb","xxhgztb":{"spider":true,"name":"信息化工作通报"}},
            {"id":"xxhzsydydxjy","xxhzsydydxjy":{"spider":true,"name":"信息化知识园地与典型经验"}},
            {"id":"dbjj","dbjj":{"spider":true,"name":"部门简介"}},
            {"id":"gzdt1","gzdt1":{"spider":true,"name":"工作动态1"}},
            {"id":"dbgz","dbgz":{"spider":true,"name":"对标工作"}},
            {"id":"glcxzs","glcxzs":{"spider":true,"name":"管理创新知识"}},
            {"id":"glcxcg","glcxcg":{"spider":true,"name":"管理创新成果"}},
            {"id":"wzlj","wzlj":{"spider":true,"name":"网站链接"}},
            {"id":"jygzdt","jygzdt":{"spider":true,"name":"交易工作动态"}},
            {"id":"mrgzap","mrgzap":{"spider":true,"name":"每日工作安排"}},
            {"id":"mzgzap","mzgzap":{"spider":true,"name":"每周工作计划"}},
            {"id":"gzzdwj","gzzdwj":{"spider":true,"name":"规章制度文件"}},
            {"id":"ydgzjh","ydgzjh":{"spider":true,"name":"月度工作计划"}},
            {"id":"jdjyxx","jdjyxx":{"spider":true,"name":"季度交易信息"}},
            {"id":"zzjs","zzjs":{"spider":true,"name":"组织建设"}},
            {"id":"cwgkmzgl","cwgkmzgl":{"spider":true,"name":"厂务公开民主管理"}},
            {"id":"scsj","scsj":{"spider":true,"name":"生产生活"}},
            {"id":"xjwb","xjwb":{"spider":true,"name":"宣教文体"}},
            {"id":"gjzjxx","gjzjxx":{"spider":true,"name":"工会综合信息"}},
            {"id":"nggz","nggz":{"spider":true,"name":"女工工作"}},
            {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
            {"id":"ddjs","ddjs":{"spider":true,"name":"党的建设"}},
            {"id":"llyxc","llyxc":{"spider":true,"name":"理论与宣传"}},
            {"id":"jjwmjs","jjwmjs":{"spider":true,"name":"精神文明建设"}},
            {"id":"tqgz","tqgz":{"spider":true,"name":"团青工作"}},
            {"id":"zl","zl":{"spider":true,"name":"总揽"}},
            {"id":"dt","dt":{"spider":true,"name":"动态"}},
            {"id":"lt","lt":{"spider":true,"name":"论坛"}},
            {"id":"jhgl","jhgl":{"spider":true,"name":"计划管理"}},
            {"id":"zbcg","zbcg":{"spider":true,"name":"招标采购"}},
            {"id":"wzgy","wzgy":{"spider":true,"name":"物资供应"}},
            {"id":"zljd","zljd":{"spider":true,"name":"质量监督"}},
            {"id":"xxzl","xxzl":{"spider":true,"name":"学习资料"}},
            {"id":"gzdt2","gzdt2":{"spider":true,"name":"工作动态2"}},
            {"id":"tydb","tydb":{"spider":true,"name":"同业对标"}},
            {"id":"gzzd","gzzd":{"spider":true,"name":"规章制度"}},
            {"id":"aqdt","aqdt":{"spider":true,"name":"安全动态"}},
            {"id":"aqjb","aqjb":{"spider":true,"name":"安全简报"}},
            {"id":"sgkb","sgkb":{"spider":true,"name":"事故快报"}},
            {"id":"sgtb","sgtb":{"spider":true,"name":"事故通报"}},
            {"id":"aqwjzd","aqwjzd":{"spider":true,"name":"安全文件制度"}},
            {"id":"aaflfg","aaflfg":{"spider":true,"name":"安全法律法规"}},
            {"id":"ldjh","ldjh":{"spider":true,"name":"领导讲话"}},
            {"id":"sgsgzzd","sgsgzzd":{"spider":true,"name":"省公司规章制度"}},
            {"id":"gwgzzd","gwgzzd":{"spider":true,"name":"国网规章制度"}},
            {"id":"jjxw","jjxw":{"spider":true,"name":"基建新闻"}},
            {"id":"xmgl","xmgl":{"spider":true,"name":"项目管理"}},
            {"id":"jjgl","jjgl":{"spider":true,"name":"技术管理"}},
            {"id":"aqgl","aqgl":{"spider":true,"name":"安全管理"}},
            {"id":"zlgl","zlgl":{"spider":true,"name":"质量管理"}},
            {"id":"zjgl","zjgl":{"spider":true,"name":"造价管理"}},
            {"id":"zhgl","zhgl":{"spider":true,"name":"综合管理"}}
            ]
        },
        {
            "key": "shandong",
            "name":"山东",
            "logname":"../Log/山东.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
                {"id":"jcdt_sjc","jcdt_sjc":{"spider":true,"name":"基层动态 市基层"}},
                {"id":"jcdt_xjc","jcdt_xjc":{"spider":true,"name":"基层动态 省供电公司"}},
                ]
        },
        {
            "key": "shanghai",
            "name":"上海",
            "logname":"../Log/上海.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gwxw","gwxw":{"spider":true,"name":"国网要闻"}},
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
                {"id":"jcxx","jcxx":{"spider":true,"name":"基层信息"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
                {"id":"hyzx","hyzx":{"spider":true,"name":"行业资讯"}},
                ]
        },
        {
            "key": "shanxi",
            "name":"山西",
            "logname":"../Log/山西.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
                {"id":"tpxw","tpxw":{"spider":true,"name":"图片新闻"}},
                {"id":"bbyw","bbyw":{"spider":true,"name":"本部要闻"}},
                {"id":"yxfc","yxfc":{"spider":true,"name":"一线风采"}},
                ]
        },
        {
            "key": "sichuan",
            "name":"四川",
            "logname":"../Log/四川.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
                ]
        },
        {
        "key": "tianjing",
        "name":"天津",
        "logname":"../Log/天津.log",
		"need_spider":false,
        "save_path":"../Data/",
        "limit_date":"20150405-20150422",
        "sections": [
            {"id":"gbyw","gbyw":{"spider":true,"name":"总部要闻"}},
            {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
            {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
            {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
            {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
            ]
        },
        {
            "key": "xinjiang",
            "name":"新疆",
            "logname":"../Log/新疆.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gwyw","gwyw":{"spider":true,"name":"国网要闻"}},
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"bbdt","bbdt":{"spider":true,"name":"本部动态"}},
                {"id":"mtjj","mtjj":{"spider":true,"name":"媒体聚焦"}},
                {"id":"gdth","gdth":{"spider":true,"name":"观点体会"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
                {"id":"yxcz","yxcz":{"spider":true,"name":"一线传真"}},
                {"id":"ztbd","ztbd":{"spider":true,"name":"专题报道"}},
                {"id":"wyyd","wyyd":{"spider":true,"name":"文艺园地"}},
                ]
        },
        {
        "key": "xintong",
        "name":"信通",
        "logname":"../Log/信通.log",
		"need_spider":false,
        "save_path":"../Data/",
        "limit_date":"20150405-20150422",
        "sections": [
            {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
            {"id":"zbdt","zbdt":{"spider":true,"name":"总部动态"}},
            {"id":"xydt","xydt":{"spider":true,"name":"行业动态"}},
            {"id":"gzysy","gzysy":{"spider":true,"name":"关注与视野"}},
            {"id":"xtjl","xtjl":{"spider":true,"name":"信通交流"}},
            ]
        },
        {
            "key": "xizang",
            "name":"西藏",
            "logname":"../Log/西藏.log",
			"need_spider":false,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"bbdt","bbdt":{"spider":true,"name":"本部动态"}},
                {"id":"gsxw","gsxw":{"spider":true,"name":"公司新闻"}},
                {"id":"jcjx","jcjx":{"spider":true,"name":"基层简讯"}},
                {"id":"yhxx","yhxx":{"spider":true,"name":"行业信息"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
                {"id":"qzlwgc_twxx","qzlwgc_twxx":{"spider":true,"name":"青藏联网工程_图文信息"}},
                ]
        },
        {
            "key": "zhejiang",
            "name":"浙江",
            "logname":"../Log/浙江.log",
			"need_spider":true,
            "save_path":"../Data/",
            "limit_date":"20150405-20150422",
            "sections": [
                {"id":"gwyw","gwyw":{"spider":true,"name":"国网要闻"}},
                {"id":"gsyw","gsyw":{"spider":true,"name":"公司要闻"}},
                {"id":"bbxw","bbxw":{"spider":true,"name":"本部新闻"}},
                {"id":"mtbd","mtbd":{"spider":true,"name":"媒体报道"}},
                {"id":"jcdt","jcdt":{"spider":true,"name":"基层动态"}},
                {"id":"tpxx","tpxx":{"spider":true,"name":"图片新闻"}},
                ]
        }

    ]
}
"""

if __name__ == '__main__':
    print demjson.decode(str)
    # print test_data
