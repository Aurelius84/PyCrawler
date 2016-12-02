# -*- coding:utf-8 -*-

"""
@version: 1.0
@author: marcovaldo
@license: Apache Licence
@contact: dsq0720@163.com
@site:
@software: PyCharm Community Edition
@file: __init__.py.py
@time: 16/12/1 下午14:09
"""

import sys
sys.path.append("..")
reload(sys)
sys.setdefaultencoding('utf8')
from myfunc import *
from scrapy.http import HtmlResponse
from collections import defaultdict
import itertools
import time
import re
import requests
import math

def goodsOutline(url):
    '''
    获取三级目录详情
    :param url: 网站主页链接
    :return: [{'url':'','first_grade':'','second_grade': '', 'third_grade': ''},...{}]
    '''
    # 存储最后的三级列表页面
    outline_data = []
    # 解析页面
    body = getHtml(url).encode('utf-8')
    html = HtmlResponse(url=url, body=str(body))
    # soup = BeautifulSoup(body, 'lxml')      # xpath不好使就用beautifulsoup
    # 抓取一级目录名及链接，这里只要以下内容：
    # 这里不要第零个（工控自动化）、第二个（五金工具）
    first_grade_name = ['工控自动化', '电工电气', '五金工具', '仪器仪表', '气动液压泵阀', '通风换热', '动力传动', '安防劳保']
    num = [1, 3, 4, 5, 6, 7]    # //*[@id="c' + str(i) + '"]/div[1]/div[1]/dt/a/text()

    for i in num:
        print('一级目录：' + first_grade_name[i])
        second_grade_name = html.xpath('//*[@id="c' + str(i) + '"]/div[1]/div/dt/a/text()').extract()
        print len(second_grade_name)
        for j in range(0, len(second_grade_name)):
            print(' 二级目录：' + second_grade_name[j])
            third_grade_name = html.xpath('//*[@id="c' + str(i) + '"]/div[1]/div['+ str(j+1) + ']/dd/a/span/text()').extract()
            third_grade_url = html.xpath('//*[@id="c' + str(i) + '"]/div[1]/div[' + str(j+1) + ']/dd/a/@href').extract()
            print len(third_grade_name)
            for k in range(len(third_grade_name)):
                url_data = defaultdict()
                url_data['url'] = 'http://www.deppre.cn/' + third_grade_url[k]
                url_data['third_grade'] = third_grade_name[k]
                print('     三级目录：' + url_data['third_grade'])
                url_data['second_grade'] = second_grade_name[j]
                url_data['first_grade'] = first_grade_name[i]
                url_data['created'] = int(time.time())
                url_data['updated'] = int(time.time())
                outline_data.append(url_data)
    print len(outline_data)
    return outline_data

def goodsUrlList(home_url):
    '''
    根据三级目录商品首页获取所有详情页url
    :param home_url:
    :return:url列表
    '''
    # 该网站不用加条件遍历所有情况就能拿到所有产品的url
    print home_url
    body = getHtml(home_url)
    html = HtmlResponse(url=home_url, body=str(body))
    url_list = []
    # 拿到该三级目录下一共有多少种产品
    num = int(html.xpath('//*[@id="pinpai"]/a[1]/text()').extract()[0][3:-1])
    # 40个产品一页
    page_num = int(math.ceil(num / 40))
    page_url = []
    page_url.append(home_url)
    for i in range(0, page_num):
        for j in range(1, 40 + 1):
            try:
                if not html.xpath('/html/body/div[5]/form[1]/ul/li['+str(j)+']/p[2]/span[1]/text()').extract()[0] == '询价':
                    url_list.append('http://www.deppre.cn/' + html.xpath('/html/body/div[5]/form[1]/ul/li['+str(j)+']/a/@href').extract()[0])
                    print('http://www.deppre.cn/' + html.xpath('/html/body/div[5]/form[1]/ul/li['+str(j)+']/a/@href').extract()[0])
            except:
                break
        page_url.append(home_url[:-5] + '-min0-max0-attr0-' + str(i+1) + '-goods_id-DESC.html')
        body = getHtml(page_url[i+1])
        html = HtmlResponse(url=page_url[i+1], body=str(body))
    print len(url_list)
    return url_list

def goodsDetail(detail_url):
    '''
    利用xpath解析关键字段
    :param detail_url: 详情页url
    :return: 因为每个详情页面可能会产生多条数据，所以返回值是一个以dict为元素的list，其中每一个dict是一条数据
    '''
    # 解析网页
    body = getHtml(detail_url).encode('utf-8')
    html = HtmlResponse(url=detail_url, body=str(body))
    print '拿到数据，正在解析...'
    # 名称
    name = '原装进口_' + html.selector.xpath('//*[@id="pic_Img"]/@alt').extract()[0]
    # 本网站下商品会有多个规格，需一次抓取多个型号和价格
    # 价格，所有的价格都在这个list中
    price_list = html.xpath('//*[@id="ECS_FORMBUY"]/div[1]/table/tr/td/span/text()').extract()
    # 型号和货期一块儿拿到
    # 详情，本网站下的商品只有p标签没有table
    detailInfo = html.xpath('//*[@id="cc1"]/div/div[2]/p/span/text()').extract()[1:]
    detailInfo = handle(detailInfo)   # 将p标签里的内容封装成符合格式的p标签
    # 图片，本网站下的商品都只有一张图片
    pic = 'http://www.deppre.cn/' + html.xpath('//*[@id="pic_Img"]/@src').extract()[0]
    goodslist = []
    for i in range(len(price_list)):
        goodslist.append(defaultdict())
        goodslist[i]['price'] = float(price_list[i][1:])
        type_lack_period = html.xpath('//*[@id="ECS_FORMBUY"]/div[1]/table/tr[' + str(3+i) + ']/td/text()').extract()
        goodslist[i]['type'] = type_lack_period[0]
        goodslist[i]['source_url'] = detail_url
        goodslist[i]['name'] = name
        goodslist[i]['detail'] = detailInfo
        goodslist[i]['pics'] = pic
        goodslist[i]['storage'] = ''
        goodslist[i]['lack_period'] = type_lack_period.pop()
        goodslist[i]['created'] = int(time.time())
        goodslist[i]['updated'] = int(time.time())
        goodslist[i]['first_grade'] = ''
        goodslist[i]['second_grade'] = ''
        goodslist[i]['third_grade'] = ''
    return goodslist


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


if __name__ == '__main__':

    # 测试函数goodsDetail(detail_url)

    url = 'http://www.deppre.cn/goods-750.html'
    detail = goodsDetail(url)
    print detail

    # 测试goodsOutline()
    # url = 'http://www.deppre.cn/'
    # goodsOutline(url)



    # 测试函数goodsOutline(url)
    # url = 'http://mro.abiz.com'
    # goodsOutline(url)

    # 测试函数goodsUrlList(home_url)
    # url = 'http://www.deppre.cn/category-125-b0.html'
    # goodsUrlList(url)