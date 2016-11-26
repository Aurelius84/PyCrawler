# -*- coding:utf-8 -*-

"""
@version: 1.0
@author: marcovaldo
@license: Apache Licence
@contact: dsq0720@163.com
@site:
@software: PyCharm Community Edition
@file: __init__.py.py
@time: 16/11/26 下午15:45
"""

# from spiders.myfunc import *
from myfunc import getHtml
from scrapy.http import HtmlResponse
from collections import defaultdict
import itertools
import time
import re
from bs4 import BeautifulSoup


def goodsUrlList(home_url):
    '''
    根据三级目录商品首页获取所有详情页url
    :param home_url: http://www.vipmro.com/search/?&categoryId=501110
    :return:url列表
    '''
    # 所有条件下的列表
    all_group_list = parseOptional(home_url)
    # 保存所有goods的详情页url
    url_list = []
    for url in all_group_list:
        # url = 'http://www.vipmro.com/search/?ram=0.9551325197768372&categoryId=501110&attrValueIds=509805,509801,509806,509807'
        # 解析html
        home_page = getHtmlFromJs(url)['content'].encode('utf-8')
        html = HtmlResponse(url=url,body=str(home_page))
        urls = html.selector.xpath('/html/body/div[7]/div[1]/ul/li/div[2]/a/@href').extract()
        url_list.extend(urls)
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
    :return: 因为每个详情页面可能会产生多条数据，所以返回值是一个以dict为元素的list，其中每一个dict是一条数据
    '''
    # 解析网页
    body = getHtml(detail_url)
    html = HtmlResponse(url=detail_url, body=str(body))
    # 根据页面中几个价格判断页面中有几个型号，然后创建几个dict
    sizes = html.xpath('//*[@id="relative_goods"]').extract()[0]
    soup = BeautifulSoup(sizes, 'lxml')
    priceslist = soup.find_all('div', {'style': 'display:none;'})   # 存储包含有价格的html语句的list
    num = len(priceslist)   # num表示了该页面中有几个产品
    prices = []     # 存储num个价格的list
    for i in range(num):
        prices.append(float(priceslist[i].string.replace('\n\t\t\t   \n              ', '').replace(' \n              ', '')))

    tmplist = soup.find_all('td')
    typelist = []  # 存储num个型号的list
    for i in range(num):
        typelist.append(tmplist[9*i+10].string)

    # 名称
    name = html.xpath('//*[@id="spec-list"]/ul/li/img/@alt').extract()[0]
    # 详情，包含两个标签
    #################################未完，待处理
    # print(html.selector.xpath('//*[@id="sub11"]/div[1]/ul/li').extract()[0])
    # exit()
    detailInfo = html.selector.xpath('//*[@id="sub11"]/div[3]/p').extract()[0]
    # 图片
    # print(html.selector.xpath('//*[@id="spec-list"]/ul/li/img'))
    pics = []
    for pic in html.selector.xpath('//*[@id="spec-list"]/ul/li/img'):
        # 去除图片尺寸,方法图片('//*[@id="spec-n1"]/img')
        pics.append( 'www.sssmro/'+ pic.xpath('@src').extract()[0])

    pics = '|'.join(pics)
    storage = ''
    lack_period = ''
    goodslist = []  # 保存num个产品dict的list
    for i in range(num):
        goodslist.append(defaultdict())
        goodslist[i]['price'] = prices[i]
        goodslist[i]['type'] = typelist[i]
        goodslist[i]['detail_url'] = detail_url
        goodslist[i]['name'] = name
        goodslist[i]['detail'] = detailInfo
        goodslist[i]['pics'] = pics
        goodslist[i]['storage'] = storage
        goodslist[i]['lack_period'] = lack_period
        goodslist[i]['created'] = int(time.time())
        goodslist[i]['updated'] = int(time.time())
    return goodslist

def parseOptional(url):
    '''
    解析url下页面各种选择项组合的url
    :param url: http://www.vipmro.com/search/?&categoryId=501110
    :return:['http://www.vipmro.com/search/?categoryId=501110&attrValueIds=509801,512680,509807,509823']
    '''
    # 解析html
    home_page = getHtmlFromJs(url)['content'].encode('utf-8')
    html = HtmlResponse(url=url,body=str(home_page))
    # 系列参数
    xi_lie = html.selector.xpath('/html/body/div[5]/div[6]/ul/li/a/@href').re(r'ValueIds=(\d+)')
    # 额定极限分断能力
    fen_duan = html.selector.xpath('/html/body/div[5]/div[10]/ul/li/a/@href').re(r'ValueIds=(\d+)')
    # 脱扣器形式
    tuo_kou_qi = html.selector.xpath('/html/body/div[5]/div[14]/ul/li/a/@href').re(r'ValueIds=(\d+)')
    # 安装方式
    an_zhuang = html.selector.xpath('/html/body/div[5]/div[12]/ul/li/a/@href').re(r'ValueIds=(\d+)')
    # 获取所有参数组合
    all_group = list(itertools.product(xi_lie,fen_duan,tuo_kou_qi,an_zhuang))
    _url = url + '&attrValueIds='
    url_list = map(lambda x:_url+','.join(list(x)),all_group)

    return url_list

if __name__ == '__main__':
    url = 'http://www.sssmro.com/goods.php?id=27203'
    llist = goodsDetail(url)
    for i in range(len(llist)):
        print(i, llist[i])

