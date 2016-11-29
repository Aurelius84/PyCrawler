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
    first_grade = u'工程机械/ 机械工业'
    # 二级目录名
    second_grade= u'通用机械'
    # 三级目录名
    third_grade_name = [u'泵阀',u'风机',u'压缩机',u'减速机']
    third_grade_url = ['http://s.hc360.com/?w=%B1%C3%B7%A7&mc=seller','http://s.hc360.com/?w=%B7%E7%BB%FA&mc=seller',
                       'http://s.hc360.com/?w=%D1%B9%CB%F5%BB%FA&mc=seller','http://s.hc360.com/?w=%BC%F5%CB%D9%BB%FA&mc=seller']
    url_data = {}
    for x in xrange (0,4):
        url_data['url'] = third_grade_url[x]
        url_data['third_grade'] = third_grade_name[x]
        url_data['second_grade'] = second_grade
        url_data['first_grade'] = first_grade
        url_data['created'] = int(time.time())
        url_data['updated'] = int(time.time())
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
    #print goods_data['name']
    # 价格
    goods_data['price'] = html.selector.xpath('//*[@id="oriPriceTop"]/text()').re(ur'[1-9]\d*\.?\d*|0\.\d*[1-9]\d*')[0]
    #print goods_data['price']
    # 型号
    goods_data['type'] = ''
    # 详情
    goods_data['detail'] = html.selector.xpath('//*[@id="pdetail"]/div[3]/table').extract()[0]
    print goods_data['detail']
    # 图片
    pics = []
    for pic in html.selector.xpath('//*[@id="thumblist"]/li/div/a/img/@src').extract():
        pics.append(pic.replace('100x100', '300x300'))
    goods_data['pics'] = ('|').join(pics)
    #print goods_data['pics']
    #库存
    goods_data['storage'] = html.selector.xpath('//*[@id="supplyInfoNum"]/text()').re(ur'[1-9]\d*\.?\d*|0\.\d*[1-9]\d*')[0]
    #print goods_data['storage']
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
    url = 'http://b2b.hc360.com/supplyself/518255479.html'
    goodsDetail(url)

