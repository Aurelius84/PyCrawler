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
from scrapy.http import HtmlResponse,Request,Response
from collections import defaultdict
import time
import chardet

def goodsUrlList(home_url):
    pass

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
    goods_data['detail'] = html.selector.xpath('/html/body/div[9]/div[2]/div[2]/table')
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

    # print(goods_data)
    return goods_data

if __name__ == '__main__':
    url = 'http://www.vipmro.com/product/587879'
    goodsDetail(url)
