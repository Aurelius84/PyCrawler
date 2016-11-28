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
# from myfunc import getHtml
from myfunc import *
from scrapy.http import HtmlResponse
from collections import defaultdict
import itertools
import time
import re
from bs4 import BeautifulSoup
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getHtmlByRequests(url):
    s = requests.session()
    headers_base = {'Connection': 'keep=alive',
                    'Content-Encoding': 'gzip',
                    'Content - Language': 'zh - CN',
                    'Content - Type': 'text / html; charset = UTF - 8',
                    'Server': 'nginx',
                    'Set - Cookie': 'clientlanguage=zh_CN; path=/',
                    'Transfer - Encoding': 'chunked',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
                    'Referer': 'http://mro.abiz.com/',}
    response = s.get(url, headers=headers_base)
    return response.content

def goodsOutline(url):
    '''
    获取三级目录详情
    :param url: 网站主页链接
    :return: [{'url':'','first_grade':'','second_grade': '', 'third_grade': ''},...{}]
    '''
    # 存储最后的三级列表页面
    outline_data = []
    # 解析页面
    body = getHtml(url)
    html = HtmlResponse(url=url, body=str(body))
    # soup = BeautifulSoup(body, 'lxml')      # xpath不好使就用beautisoup
    # 抓取一级目录名及链接，这里只要以下内容：
    # 这里不要第四个（办公、仓储及物流用品）、第五个（仪器仪表、金属加工、焊接）
    first_grade_name = ['安防、劳保、清洁', '手工具、动力工具及耗材', '电气、管道、暖通照明', '机械部件、设备条件']
    num = ['1', '2', '3', '6']
    for i in range(4):
        second_grade_name = []
        q = 1
        while(True):
            try:
                second_grade_name.append(
                html.xpath('/html/body/div[3]/div[1]/div[2]/div/div[' + num[i] + ']/div/div[1]/dl[' + str(q) + ']/dt/a/text()').extract()[0])
                q += 1
            except:
                break
        for j in range(0, len(second_grade_name)):
            third_grade_name = html.xpath('/html/body/div[3]/div[1]/div[2]/div/div[' + num[i] + ']/div/div[1]/dl['+ str(j+1)+']/dd/a/text()').extract()
            third_grade_url = html.xpath('/html/body/div[3]/div[1]/div[2]/div/div[' + num[i] + ']/div/div[1]/dl['+str(j+1)+']/dd/a/@href').extract()
            for k in range(len(third_grade_name)):
                url_data = defaultdict()
                url_data['url'] = url + third_grade_url[k]
                url_data['third_grade'] = third_grade_name[k]
                url_data['second_grade'] = second_grade_name[j]
                url_data['first_grade'] = first_grade_name[i]
                url_data['created'] = int(time.time())
                url_data['updated'] = int(time.time())
                outline_data.append(url_data)
    return outline_data

def goodsUrlList(home_url):
    '''
    根据三级目录商品首页获取所有详情页url
    :param home_url: http://www.sssmro.com//category.php?id=1137&price_min=&price_max=
    :return:url列表
    '''
    # 该网站不用加条件遍历所有情况就能拿到所有产品的url
    body = getHtmlByRequests(home_url)
    html = HtmlResponse(url=home_url, body=str(body))
    url_list = []
    # 拿到该三级目录下一共有几页产品，存在变量num中
    num = int(html.xpath('//*[@id="tableForm"]/div[2]/span[2]/text()').extract()[0][1:-1])
    for i in range(1, num+1):
        url = home_url[:-4] + '_' + str(i) + '.htm' # 第i页
        body = getHtmlByRequests(url)
        html = HtmlResponse(url=url, body=str(body))
        tmp_list = html.xpath('//*[@id="tableForm"]/div[1]/ul/li/p[1]/a/@href').extract()
        for tmp in tmp_list:
            url_list.append('http://mro.abiz.com' + tmp)
    return url_list


def goodsDetail(detail_url):
    '''
    利用xpath解析关键字段
    :param detail_url: 详情页url
    :return: 因为每个详情页面可能会产生多条数据，所以返回值是一个以dict为元素的list，其中每一个dict是一条数据
    '''
    # 解析网页

    body = getHtmlByRequests(detail_url)
    print body
    html = HtmlResponse(url=detail_url, body=str(body))

    goods_data = defaultdict()
    # 名称
    goods_data['name'] = html.xpath('//*[@id="productMainName"]/text()').extract()[0]
    # 价格
    goods_data['price'] = html.selector.xpath('/html/body/div[5]/div/div[2]/div[2]/div[1]/dl[1]/dd/strong/b/text()').extract()
    # 型号
    goods_data['type'] = html.selector.xpath('/html/body/div[5]/div/div[2]/div[2]/div[1]/div/dl[2]/dd/text()').extract()[0]
    # 详情    table放在了一个iframe里面，需要访问一个新的链接
    tmp_url = 'http://mro.abiz.com/' + html.selector.xpath('//*[@id="rightFrame"]/@src').extract()[0]
    tmp = getHtmlByRequests(tmp_url)
    tmp = HtmlResponse(url=tmp_url, body=str(tmp))
    goods_data['detail'] = tmp.selector.xpath('/html/body/div/table').extract()[0]
    # 图片，下面的while循环抓取多张图片，并拿到那张尺寸大的链接
    pics = []
    index = 1
    while(index):
        try:
            tmp_url = str(html.xpath('//*[@id="detailPictureSlider"]/li['+str(index)+']/img/@src').extract()[0])[:-6] + '2.jspx'
            pics.append('http://mro.abiz.com' + tmp_url)
            index += 1
        except:
            break
    goods_data['pics'] = '|'.join(pics)
    goods_data['storage'] = ''
    goods_data['lack_period'] = re.findall(r'\d*',
                                           str(html.xpath('/html/body/div[5]/div/div[2]/div[2]/div[1]/div/dl[4]/dd/text()').extract()[0]))[0]
    goods_data['created'] = int(time.time())
    goods_data['updated'] = int(time.time())
    return goods_data

def parseOptional(url):
    '''
    解析url下页面各种选择项组合的url
    :param url: http://www.vipmro.com/search/?&categoryId=501110
    :return:['http://www.vipmro.com/search/?categoryId=501110&attrValueIds=509801,512680,509807,509823']
    '''
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
    all_group = list(itertools.product(xi_lie, fen_duan, tuo_kou_qi, an_zhuang))
    _url = url + '&attrValueIds='
    url_list = map(lambda x: _url+','.join(list(x)), all_group)

    return url_list
    '''
    pass


if __name__ == '__main__':

    # 测试函数goodsDetail(detail_url)
    # url = 'http://mro.abiz.com/product/AB1000.htm'
    # print goodsDetail(url)

    # 测试函数goodsOutline(url)
    # url = 'http://mro.abiz.com'
    # goodsOutline(url)

    # 测试函数goodsUrlList(home_url)
    url = 'http://mro.abiz.com/catalog/63011.htm'
    goodsUrlList(url)