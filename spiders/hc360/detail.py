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
import time
import re
from StringIO import StringIO
import gzip
import zlib



def goodsOutline():
    '''
    获取三级目录详情
    :param url:网站主页
    :return:[{'url':'','first_grade':'',...},...{}]
    '''
    # 存储各级分类信息
    outline_data = []
    # 解析页面
    # body = getHtml(url)
    # html = HtmlResponse(url=url,body=body)
    # 一级类目名
    first_grade = u'工程机械/ 机械工业'
    # 二级目录名
    second_grade= u'通用机械'
    # 三级目录名
    third_grade_name = [u'泵阀',u'风机',u'压缩机',u'减速机']
    third_grade_url = ['http://s.hc360.com/?w=%B1%C3%B7%A7&mc=seller','http://s.hc360.com/?w=%B7%E7%BB%FA&mc=seller',
                       'http://s.hc360.com/?w=%D1%B9%CB%F5%BB%FA&mc=seller','http://s.hc360.com/?w=%BC%F5%CB%D9%BB%FA&mc=seller']
    for i in xrange(4):
        # 获取三级目录home页下各个条件url
        url_list = parse(third_grade_url[i])
        for j in xrange(len(url_list)):
            url_data = defaultdict()
            url_data['url'] = url_list[j]
            url_data['third_grade'] = third_grade_name[i]
            url_data['second_grade'] = second_grade
            url_data['first_grade'] = first_grade
            url_data['created'] = int(time.time())
            url_data['updated'] = int(time.time())
            outline_data.append(url_data)
        # print(outline_data)
        # exit()
    return outline_data

def goodsUrlList(home_url):
    '''
    根据三级目录商品首页获取所有详情页url
    :param home_url: http://www.vipmro.com/search/?&categoryId=501110
    :return:url列表
    '''
    # 保存所有goods的详情页url
    url_list = []
    # 解析html
    buff = StringIO(getHtmlByVPN(home_url))
    f = gzip.GzipFile(fileobj=buff)
    home_page = f.read().decode('gb18030').encode('utf8')
    html = HtmlResponse(url=home_url,body=home_page)
    # 获取总数
    total_num = html.selector.xpath('/html/body/div[3]/div[3]/span/em/text()').re(r'(\d+)')
    if not total_num:
        return False
    # 合计总页数
    total_num = int(total_num[0])
    if total_num > 7000:
        total_num = 7000
    total_page = total_num/20
    # 获取关键get参数
    get_data = home_url.split('?')[1][:-1]
    for i in xrange(int(total_page)):
        cur_home_url = 'http://s.hc360.com/?{0}&af=2&afadprenum=0&afadval=0&afadbeg={1}'.format(get_data,20*i)
        # 解析页面
        print(cur_home_url)
        # buff = StringIO(getHtmlByVPN(cur_home_url))
        # f = gzip.GzipFile(fileobj=buff)
        # home_page = f.read().decode('gb18030').encode('utf8')
        d = zlib.decompressobj(16+zlib.MAX_WBITS)
        try:
            home_page = d.decompress(getHtmlByVPN(cur_home_url)).decode('gb18030').encode('utf8')
            html = HtmlResponse(url=cur_home_url,body=home_page)
        except Exception,e:
            print(Exception,e)
            continue
        cur_url_list = html.selector.xpath('/html/body/li/div[1]/div[2]').re('http:\/\/b2b\.hc360\.com\/supplyself/\d+\.html')
        # /html/body/div[3]/div[5]/div[2]/div[2]/ul[1]/li[2]
        # /html/body/div[3]/div[5]/div[2]/div[2]/ul[2]/li[2]
        # /html/body/div[3]/div[5]/div[2]/div[2]/ul[2]/ul/li[1]
        cur_url_list = list(set(cur_url_list))
        url_list.extend(cur_url_list)
        print(len(cur_url_list))

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

    # print(goods_data)
    return goods_data

def parse(url):
    '''
    解析url下页面各种选择项组合的url
    :param url: http://s.hc360.com/?w=%B1%C3%B7%A7&mc=seller
    :return:['http://www.vipmro.com/search/?categoryId=501110&attrValueIds=509801,512680,509807,509823']
    '''
    # u'泵阀',u'风机',u'压缩机',u'减速机'
    third_xpath = {'%B1%C3%B7%A7':
                       ['//*[@id="list_layout_h2"]/div[2]/ul/li/a/@href'],# 材质
                   '%B7%E7%BB%FA':
                       ['//*[@id="list_layout_h6"]/div[2]/ul/li/a/@href'],# 气流方向
                   '%D1%B9%CB%F5%BB%FA':
                       ['//*[@id="list_layout_h1"]/div[2]/ul/li/a/@href'],# 类型
                   '%BC%F5%CB%D9%BB%FA':
                       ['//*[@id="list_layout_h1"]/div[2]/ul/li/a/@href']}# 品牌

    for i in xrange(len(third_xpath.keys())):
        pattern = third_xpath.keys()[i]
        if re.search(re.compile(pattern),url):
            break

    # 解析html
    buff = StringIO(getHtmlByVPN(url))
    # gzip解压
    f = gzip.GzipFile(fileobj=buff)
    body = f.read().decode('gb18030').encode('utf8')

    html = HtmlResponse(url=url,body=body,)
    # 考虑各种参数组合的三级分类地址
    url_list = html.selector.xpath(third_xpath[pattern][0]).extract()

    return url_list

if __name__ == '__main__':
    # url = 'http://b2b.hc360.com/supplyself/518255479.html'
    # url = 'http://s.hc360.com/cgi-bin/mmts?newurl=2&w=%B1%C3%B7%A7&mc=seller&h=DCE4297FABADA215'
    print goodsOutline()

