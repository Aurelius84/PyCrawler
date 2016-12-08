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
# import sys
# sys.path.append('..')
# from myfunc import *
from spiders.myfunc import *
from scrapy.http import HtmlResponse
from collections import defaultdict
import itertools
import time
import json
import re

def goodsOutline():
    '''
    获取三级目录详情
    :param url:网站主页
    :return:[{'url':'','first_grade':'',...},...{}]
    '''
    # 存储各级分类信息
    # //*[@id="mod-catpanel-id"]/li[8]/div/div/div[1]/div/div[1]/div[2]/a[1]
    # //*[@id="mod-catpanel-id"]/li[8]/div/div/div[1]/div/div[2]/div[2]/a[1]
    url = 'https://yqyb.1688.com/'
    outline_data = []
    # 解析页面
    body = getHtmlByVPN(url)
    html = HtmlResponse(url=url,body=body)
    # 一级类目名
    first_grade = '电工测量仪器'
    # 二级类目名
    second_grade = '电工测量仪器'
    # 列表页id
    urls = html.selector.xpath('//*[@id="mod-catpanel-id"]/li[8]/div/div/div[1]/div/div[1]/div[2]/a/@href').re('\-\-(\d+)')
    # 三级目录名
    third_grades = html.selector.xpath('//*[@id="mod-catpanel-id"]/li[8]/div/div/div[1]/div/div[1]/div[2]/a/text()').extract()
    # 分开抓
    urls.extend(html.selector.xpath('//*[@id="mod-catpanel-id"]/li[8]/div/div/div[1]/div/div[2]/div[2]/a[1]/@href').re('\-\-(\d+)'))
    third_grades.extend(html.selector.xpath('//*[@id="mod-catpanel-id"]/li[8]/div/div/div[1]/div/div[2]/div[2]/a[1]/text()').extract())
    for i in xrange(len(urls)):
        # 格式化数据
        url_data = defaultdict()
        url_data['url'] = 'https://s.1688.com/selloffer/offer_search.htm?priceStart=0.01&uniqfield=pic_tag_id&n=y&filt=y#sm-filtbar&categoryId={0}'.format(urls[i])
        url_data['third_grade'] = third_grades[i]
        url_data['second_grade'] = second_grade
        url_data['first_grade'] = first_grade
        url_data['created'] = int(time.time())
        url_data['updated'] = int(time.time())
        # 保存
        outline_data.append(url_data)

    # 补全剩下几个三级目录
    urls_id = [141907,1425,141906,1031666,922,1032539,1032538]
    third_grade = ['阀门','水泵','禁锢链接','输送设备','矿山施工设备','矿山输送设备','矿山装卸设备']
    for j in range(len(urls_id)):
        # 格式化数据
        url_data = defaultdict()
        url_data['url'] = 'https://s.1688.com/selloffer/offer_search.htm?priceStart=0.01&uniqfield=pic_tag_id&n=y&filt=y#sm-filtbar&categoryId={0}'.format(urls_id[j])
        url_data['third_grade'] = third_grade[j]
        url_data['second_grade'] = '矿山及其行业设备'
        url_data['first_grade'] = '矿山及其行业设备'
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
    urls = []
    # 转换为接口地址
    url_id = re.search('Id=(\d+)',home_url).group(1)
    pre_url = 'https://s.1688.com/selloffer/rpc_async_render.jsonp?categoryId={0}&n=y&filt=y&priceStart=0.1&qrwRedirectEnabled=false&uniqfield=pic_tag_id&templateConfigName=marketOfferresult&offset=8&pageSize=60&asyncCount=60&startIndex=0&pageOffset=2&async=true&enableAsync=true&rpcflag=new&_pageName_=market&beginPage='.format(url_id)
    # 解析html
    import zlib
    for page in xrange(100):
        # 解析html
        object_ids = ''
        try:
            d = zlib.decompressobj(16+zlib.MAX_WBITS)
            home_page = d.decompress(getHtmlByVPN(pre_url+str(page+1),http_type='https')).decode('gbk')
            object_ids = re.search('object_ids.*?category_id',home_page).group(0)
            # 解析html
            # print home_page
        except Exception,e:
            print(Exception,e)
        goods_id = re.findall('\d{6,20}', object_ids)
        print('fetch {0} urls.'.format(len(goods_id)))
        url_format = 'https://detail.1688.com/offer/{0}.html'
        urls.extend(map(lambda x:url_format.format(x),set(goods_id)))

    return list(set(urls))

def goodsDetail(detail_url):
    '''
    利用xpath解析关键字段
    :param detail_url: 详情页url
    :return: 各个字段信息 dict
    '''
    goods_data = defaultdict()
    try:
        # 详情页链接
        goods_data['source_url'] = detail_url
        # 解析html body必须是str类型
        body = getHtmlByVPN(detail_url).decode('gbk').encode('utf8')
        # print(body)
        html = HtmlResponse(url=detail_url,body=body,encoding='utf8')
        # 名称
        goods_data['name'] = html.xpath('//*[@id="mod-detail-title"]/h1/text()').extract()[0]
        # 价格
        try:
            goods_data['price'] = html.xpath('//*[@id="mod-detail-price"]/div/table/tr[1]/td[2]/div/span[2]/text()').extract()[0]
        except:
            goods_data['price'] = html.xpath('//*[@id="mod-detail-price"]/div/table/tr[1]/td[2]/span[2]/text()').extract()[0]
        # 参数名
        names = html.selector.xpath('//*[@id="mod-detail-attributes"]/div[1]/table/tbody/tr/td[contains(@class,"de-feature")]/text()').extract()
        params = html.selector.xpath('//*[@id="mod-detail-attributes"]/div[1]/table/tbody/tr/td[contains(@class,"de-value")]/text()').extract()
        type = ''
        if names and len(names) == len(params):
            type = params[names.index(u'型号')]
        # 型号
        goods_data['type'] = type
        # 详情
        goods_data['detail'] = handleTable(names, params)
        # 图片
        pics = []
        for pic in html.selector.xpath('//*[@id="dt-tab"]/div/ul/li/@data-imgs').extract():
            # 去除图片尺寸,方法图片
            # print(pic)
            pics.append(json.loads(pic)['original'])

        goods_data['pics'] = '|'.join(pics)
        try:
            goods_data['storage'] = html.selector.xpath('//*[@id="mod-detail-bd"]/div[2]/div[11]/div/div/div/div[1]/div[2]/table/tr[1]/td[3]/span/em[1]/text()').extract()[0]
        except:
            goods_data['storage'] = re.findall(r'\d+', html.xpath('//*[@id="mod-detail-bd"]/div[2]/div[12]/div/div/div[1]/div[2]/span/text()').extract()[0])[0]

        goods_data['lack_period'] = ''
        goods_data['created'] = int(time.time())
        goods_data['updated'] = int(time.time())
    except Exception,e:
         print(Exception,e)

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
    # 测试函数goodsUrlList
    url = 'https://s.1688.com/selloffer/offer_search.htm?priceStart=0.1&uniqfield=pic_tag_id&categoryId=1033834&n=y&filt=y#sm-filtbar'
    # url = 'https://s.1688.com/selloffer/--1033826.html?spm=a260b.7624510.1998298138.232.i7Asax'
    # print goodsUrlList(url)

    # 测试函数goodsDetail
    url = 'https://detail.1688.com/offer/534922977173.html'
    print goodsDetail(url)
