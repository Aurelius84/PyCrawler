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
import time
import re
import io
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
    goods_data = defaultdict()
    # 详情页链接
    goods_data['source_url'] = detail_url
    # 解析html body必须是str类型
    body = getHtml(detail_url).decode('gb18030').encode('utf-8')
    html = HtmlResponse(url=detail_url, body=str(body),encoding='utf-8')
    # 名称
    goods_data['name'] = html.xpath('//*[@id="comTitle"]/text()').extract()[0]
    print goods_data['name']
    # 价格
    goods_data['price'] = html.selector.xpath('//*[@id="oriPriceTop"]/text()').re(ur'[1-9]\d*\.?\d*|0\.\d*[1-9]\d*')[0]
    print goods_data['price']
    # 型号
    goods_data['type'] = ''
    # 详情
    detaildiv = html.selector.xpath('//*[@id="pdetail"]')
    detail_table = '\n'.join(detaildiv.xpath('//table').extract())
    detail_p = ''.join(detaildiv.xpath('//p').extract())
    goods_data['detail'] = detail_table + detail_p
    print goods_data['detail']
    goods_data['detail'] = re.sub(ur'^<img.*>$', '', goods_data['detail'])
    f = open('detail.txt', 'w')
    f.write(goods_data['name'].encode('utf-8'))
    f.write(goods_data['detail'].encode('utf-8'))
    f.close()
    # 图片
    pics = []
    for pic in html.selector.xpath('//*[@id="thumblist"]/li/div/a/img/@src').extract():
        pics.append(pic.replace('100x100', '300x300'))
    goods_data['pics'] = ('|').join(pics)
    print goods_data['pics']
    #库存
    goods_data['storage'] = html.selector.xpath('//*[@id="supplyInfoNum"]/text()').re(ur'[1-9]\d*\.?\d*|0\.\d*[1-9]\d*')[0]
    print goods_data['storage']
    #供货时间
    goods_data['lack_period'] = ''
    goods_data['created'] = int(time.time())
    goods_data['updated'] = int(time.time())

    # print(goods_data['detail'])
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

if __name__ == '__main__':
    # url = 'http://www.vipmro.com/product/587879'
    url = 'http://b2b.hc360.com/supplyself/605891383.html'
    goodsDetail(url)

