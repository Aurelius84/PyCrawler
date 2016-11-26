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

from spiders.myfunc import *
from scrapy.http import HtmlResponse
from collections import defaultdict
import itertools
import time


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
    :return: 各个字段信息 dict
    '''
    goods_data = defaultdict()
    # 详情页链接
    goods_data['source_url'] = detail_url
    # 解析html body必须是str类型
    body = getHtmlFromJs(detail_url)['content'].encode('utf-8')
    html = HtmlResponse(url=detail_url,body=str(body))
    # 名称
    goods_data['name'] = html.xpath('/html/body/div[7]/div[2]/h1/text()').extract()[0]
    # 价格
    goods_data['price'] = html.selector.xpath('/html/body/div[7]/div[2]/div[2]/ul/li[1]/label[1]/text()').extract()[0]
    # 型号
    goods_data['type'] = html.selector.xpath('/html/body/div[7]/div[2]/div[2]/ul/li[3]/label/text()').extract()[0]
    # 详情
    goods_data['detail'] = html.selector.xpath('/html/body/div[9]/div[2]/div[2]/table').extract()[0]
    # 图片
    pics = []
    for pic in html.selector.xpath('/html/body/div[7]/div[1]/div[2]/div[2]/ul/li/img'):
        # 去除图片尺寸,方法图片
        pics.append(pic.xpath('@src').extract()[0].replace('!240240',''))
    goods_data['pics'] = '|'.join(pics)
    goods_data['storage'] = ''
    goods_data['lack_period'] = ''
    goods_data['created'] = int(time.time())
    goods_data['updated'] = int(time.time())

    # print(goods_data['detail'])
    return goods_data

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
    # url = 'http://www.vipmro.com/product/587879'
    url = 'http://www.vipmro.com/search/?&categoryId=501110'
    goodsUrlList(url)
    print("it works")

