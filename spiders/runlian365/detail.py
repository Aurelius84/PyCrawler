# -*- coding:utf-8 -*-

"""
@version: 1.0
@author: kevin
@license: Apache Licence 
@contact: liujiezhang@bupt.edu.cn
@site: 
@software: PyCharm Community Edition
@file: detail.py
@time: 16/11/25 上午10:57
"""

from myfunc import *
from scrapy.http import HtmlResponse
from collections import defaultdict
import itertools
import time
import re
import chardet

def goodsOutline(url):
    '''
    获取三级目录详情
    :param url:网站主页
    :return:[{'url':'','first_grade':'',...},...{}]
    '''
    # 存储各级分类信息
    outline_data = []
    # 解析页面
    body = getHtml(url)
    html = HtmlResponse(url=url,body=body)
    # 一级类目名
    first_grade = [u'建筑 矿用 防爆',u'泵 阀门']
    #预存一部分XPATH的基址
    basepath = ['//*[@id="newpro101"]/div[2]/ul','//*[@id="newpro401"]/div[2]/ul']
    #//*[@id="newpro4"]/h3/a 泵 阀门 
    for i in xrange(len(first_grade)):
        # 二级类目名
        if i == 0: 
            #建筑 矿用 防爆
            second_grade = html.selector.xpath(basepath[i]+u'/li/b/a/text()').extract()[1:9]
        else:
            second_grade = html.selector.xpath(basepath[i]+u'/li/b/a/text()').extract()
        #print u'二级目录个数' + str(len(second_grade))
        for j in xrange(len(second_grade)):
            # 三级类目名和链接url
            # //*[@id="newpro101"]/div[2]/ul/li[3]/a[1]
            #//*[@id="newpro401"]/div[2]/ul/li[6]/a[1]
            if i == 0:
                third_grade_name = html.selector.xpath(basepath[i]+'/li[{0}]/a/text()'.format(j+2)).extract()
                third_grade_url = html.selector.xpath(basepath[i]+'/li[{0}]/a/@href'.format(j+2)).extract()
            else:
                third_grade_name = html.selector.xpath(basepath[i]+'/li[{0}]/a/text()'.format(j+1)).extract()
                third_grade_url = html.selector.xpath(basepath[i]+'/li[{0}]/a/@href'.format(j+1)).extract()
            print('三级目录个数：'+str(len(third_grade_name)))
            for k in xrange(len(third_grade_name)):
                # 格式化数据
                url_data = defaultdict()
                url_data['url'] ='http://www.runlian365.com/' + third_grade_url[k]
                url_data['third_grade'] = third_grade_name[k]
                url_data['second_grade'] = second_grade[j]
                url_data['first_grade'] = first_grade[i]
                url_data['created'] = int(time.time())
                url_data['updated'] = int(time.time())
                
                #print  url_data['first_grade'] + ':' + url_data['second_grade']+ ':'+url_data['third_grade']
                # 保存
                outline_data.append(url_data)
            

    return outline_data

 

def goodsUrlList(home_url):
    '''
    根据三级目录商品首页获取所有详情页url
    :param home_url: http://www.vipmro.com/search/?&categoryId=501110
    :return:url列表
    '''
    # 网站基址
    base = u'http://www.runlian365.com'
    # 所有条件下的列表
    all_group_list = parse(home_url)
    # 保存所有goods的详情页url
    url_list = []
    for url in all_group_list:
        # url = 'http://www.vipmro.com/search/?ram=0.9551325197768372&categoryId=501110&attrValueIds=509805,509801,509806,509807'
        # 解析html
        home_page = getHtml(url)
        html = HtmlResponse(url=url,body=str(home_page))
        urls = html.selector.xpath('/html/body/div[5]/div/div[2]/div/div[1]/div/div/h4/a/@href').extract()
        url_list.extend(urls)
    for x in xrange(0,len(url_list)):
        url_list[x] = base + url_list[x]
        print str(x) + url_list[x] 


    #     print(len(urls))
    #     print(urls)
    #     exit()
    # print(len(url_list))
    # print(url_list)
    return url_list

def goodsDetail(detail_url):
    '''
    利用xpath解析关键字段
    :param detail_url: 详情页url
    :return: 各个字段信息 dict
    '''
    print detail_url
    starttime = time.time()
    goods_data = defaultdict()
    # 详情页链接
    goods_data['source_url'] = detail_url
    # 解析html body必须是str类型
    try:
        body = getHtml(detail_url)
    except:
        print 'err getHtml()'

    #print body
    html = HtmlResponse(url=detail_url,body=str(body))
    # 名称
    try:
        goods_data['name'] = html.xpath('/html/body/div[4]/div[2]/div/h1/a/text()').extract()[0]
    except:
        goods_data['name'] = ''
        print 'err in getting name '
    # 价格(为毛啊1.sub函数第二个参数设置为空输出就没了2.对价格做个lstrip()输出又没了)
    try:
        goods_data['price'] = float(html.selector.xpath('/html/body/div[4]/div[2]/div/div[1]/div[2]/div[1]/p[1]/b/text()').re(ur'[1-9]\d*\.?\d*|0\.\d*[1-9]\d*')[0])
    except:
        goods_data['price'] = float(0)
        print 'err in getting price'
    #print goods_data['price']
    # 型号
    try:
        goods_data['type'] = re.sub(ur'^.{3}','',html.selector.xpath('/html/body/div[4]/div[2]/div/div[1]/div[2]/div[1]/p[2]/span[1]/font[2]/text()').extract()[0],count = 1)
    except:
        goods_data['type'] = ''
        print 'err in getting type'
    # 详情
    try:
        detail_p = html.selector.xpath(
            '/html/body/div[4]/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[1]//p/text()').extract()
        detail_p = handle(detail_p)
        #goods_data['detail'] = detail_p
        table_name = html.selector.xpath(
            '/html/body/div[4]/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/table/tr/td/text()').extract()
        table_para = html.selector.xpath(
            '/html/body/div[4]/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/table/tr/td/div/text()').extract()
        detail_table = handleTable(table_name, table_para)
        goods_data['detail'] = detail_table + detail_p
    except:
        goods_data['detail'] = ''
        print 'err in getting detail'

    # 图片
    try:
        goods_data['pics'] = html.selector.xpath('//*[@id="proSmallImg"]').xpath('@src').extract()[0].replace('../','http://www.runlian365.com/')
    except:
        goods_data['pics'] = ''
        print 'Err happens getting pictures==!'
    goods_data['storage'] = ''
    goods_data['lack_period'] = ''
    goods_data['created'] = int(time.time())
    goods_data['updated'] = int(time.time())

    # print(goods_data['detail'])
    endtime = time.time()
    print 'done in '+ str(endtime - starttime )+ 's'
    return goods_data

def parse(url):
    '''
    解析url下页面各种选择项组合的url
    :param url: http://www.vipmro.com/search/?&categoryId=501110
    :return:['http://www.vipmro.com/search/?categoryId=501110&attrValueIds=509801,512680,509807,509823']
    '''
    # 解析html
    home_page = getHtml(url)
    html = HtmlResponse(url=url,body=str(home_page))
    #总页数
    page_total = 1
    #三级列表下所有
    url_list = []
    if html.selector.xpath('/html/body/div[5]/div/div[2]/div/div[2]/div/a[@class = "pages_next"]'):
        page_total = html.selector.xpath('/html/body/div[5]/div/div[2]/div/div[2]/div/a[last()-1]/text()').extract()[0].replace('...','')
    elif html.selector.xpath('/html/body/div[5]/div/div[2]/div/div[2]/div/a[last()]/text()'):
        page_total = html.selector.xpath('/html/body/div[5]/div/div[2]/div/div[2]/div/a[last()]/text()').extract()[0]
    for x in xrange(1,int(page_total)+1):
        url_list.append(url.replace('.html','-'+ str(x) + '.html'))
    return url_list

def handle(pLabel):
    """
    # 处理p标签
    :param pLabel: p标签中包含的内容
    :return: 符合要求的p标签语句
    """
    label = '<p>产品介绍：</p>\n'
    for s in pLabel:
        label += '<p>' + s.encode('utf-8').replace('\n', '') + '</p>\n'
    label = unicode(label, 'utf-8')
    # 格式
    font = '<style>.default p{padding:0;margin:0;font-family:微软雅黑;' \
           'font-size:18px;' \
           'line-height:28px;color:#333;' \
           'width:780px;text-indent:-5rem;margin-left:6.2rem}</style>'
    font = unicode(font, 'utf-8')
    return label + font

def handleTable(table_name,table_param):
    '''
    格式化table
    :param table_name:参数名
    :param table_param:参数
    :return:table
    '''

    table = u'''<table border="1" cellpadding="0" cellspacing="0" width="100%"><tbody><tr><th colspan="2">产品参数</th></tr>'''

    for i in xrange(len(table_name)):
        line = u'''<tr><td class="name">{0}</td><td class="nr">{1}</td></tr>'''.format(table_name[i],table_param[i])
        table += line

    table += u'''</tbody></table><style>.default td{padding:2px 8px;border-right:1px solid #D8D8D8;border-bottom:1px solid #D8D8D8;}.default table{border-left:1px solid #D8D8D8;border-top:1px solid #D8D8D8;margin:10px 0}.default th{border-bottom:1px solid #D8D8D8;border-right:1px solid #D8D8D8;}.name{width:50%}</style>'''

    return table

if __name__ == '__main__':
    # url = 'http://www.runlian365.com/chanpin/xx-14.html'
    url = 'http://www.runlian365.com/chanpin/xx-9031.html'
    goodsDetail(url)

