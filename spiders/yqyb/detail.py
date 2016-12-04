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
import json

def goodsOutline(url):
    '''
    获取三级目录详情
    :param url:网站主页
    :return:[{'url':'','first_grade':'',...},...{}]
    '''
    # 存储各级分类信息
    outline_data = []
    # 解析页面
    body = getHtmlFromJs(url)['content'].encode('utf-8')
    html = HtmlResponse(url=url,body=body)
    # 一级类目名
    first_grade = html.selector.xpath('/html/body/div[3]/div/ul/li[1]/div/div[1]/ul/li/a/text()').extract()
    # 去掉后两个
    for i in xrange(len(first_grade)-2):
        # 二级类目名
        #/html/body/div[3]/div/ul/li[1]/div/div[2]/div[1]/div[1]
        #/html/body/div[3]/div/ul/li[1]/div/div[2]/div[3]/div[1]
        second_grade = html.selector.xpath('/html/body/div[3]/div/ul/li[1]/div/div[2]/div[{0}]/div/span/a/text()'.format(i+1)).extract()
        print('second: {0}'.format(len(second_grade)))
        for j in xrange(len(second_grade)):
            # 三级类目名和链接url
            # /html/body/div[3]/div/ul/li[1]/div/div[2]/div[1]/div[1]/ul/li[1]/a
            # /html/body/div[3]/div/ul/li[1]/div/div[2]/div[1]/div[2]/ul/li[1]/a
            third_grade_name = html.selector.xpath('/html/body/div[3]/div/ul/li[1]/div/div[2]/div[{0}]/div[{1}]/ul/li/a/text()'.format(i+1,j+1)).extract()
            third_grade_url = html.selector.xpath('/html/body/div[3]/div/ul/li[1]/div/div[2]/div[{0}]/div[{1}]/ul/li/a/@href'.format(i+1,j+1)).extract()
            print(len(third_grade_name))
            for k in xrange(len(third_grade_name)):
                # 格式化数据
                url_data = defaultdict()
                url_data['url'] = third_grade_url[k]
                url_data['third_grade'] = third_grade_name[k]
                url_data['second_grade'] = second_grade[j]
                url_data['first_grade'] = first_grade[i]
                url_data['created'] = int(time.time())
                url_data['updated'] = int(time.time())
                # 保存
                outline_data.append(url_data)
    return outline_data


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
        if not urls:
            continue
        url_list.extend(urls)
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
    body = getHtml(detail_url).decode('gbk').encode('utf8')
    # print(body)
    html = HtmlResponse(url=detail_url,body=body,encoding='utf8')
    # 名称
    goods_data['name'] = html.xpath('//*[@id="mod-detail-title"]/h1/text()').extract()[0]
    # 价格
    goods_data['price'] = html.selector.xpath('//*[@id="mod-detail-price"]/div/table/tr[1]/td[2]/div/span[2]/text()').extract()[0]
    # 参数名
    names = html.selector.xpath('//*[@id="mod-detail-attributes"]/div[1]/table/tbody/tr/td[contains(@class,"de-feature")]/text()').extract()
    params = html.selector.xpath('//*[@id="mod-detail-attributes"]/div[1]/table/tbody/tr/td[contains(@class,"de-value")]/text()').extract()
    type = ''
    if names and len(names) == len(params):
        type = params[names.index(u'型号')]
    # 型号
    goods_data['type'] = type
    # 详情
    goods_data['detail'] = handleTable(names,params)
    # 图片
    pics = []
    for pic in html.selector.xpath('//*[@id="dt-tab"]/div/ul/li/@data-imgs').extract():
        # 去除图片尺寸,方法图片
        # print(pic)
        pics.append(json.loads(pic)['original'])

    goods_data['pics'] = '|'.join(pics)
    goods_data['storage'] = html.selector.xpath('//*[@id="mod-detail-bd"]/div[2]/div[11]/div/div/div/div[1]/div[2]/table/tr[1]/td[3]/span/em[1]/text()').extract()[0]

    goods_data['lack_period'] = ''
    goods_data['created'] = int(time.time())
    goods_data['updated'] = int(time.time())
    # except Exception,e:
    #     print(Exception,e)

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
    # url = 'http://www.vipmro.com/search/?&categoryId=501110'
    url = 'https://detail.1688.com/offer/520658508585.html?tracelog=p4p'
    print goodsDetail(url)
