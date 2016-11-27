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
                    'Date': 'Sun, 27 Nov 2016 10:12:37 GMT',
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
    soup = BeautifulSoup(body, 'lxml')      # xpath不好使就用beautisoup
    # 抓取一级目录名及链接，这里只要以下内容：
    # 泵阀门接头管件（不要化工泵）、紧固件密封件传动件（全要）、仪器仪表测量（只要气体检测仪，电力电工检测仪器）
    # 所以现在一级列表名称及链接不抓了，直接放到下面
    first_grade_name = ['紧固件密封件传动件', '泵阀门接头管件', '仪器仪表测量']
    first_grade_url = [url + '/category.php?id=207&amp;price_min=&amp;price_max=',
                       url + '/category.php?id=208&amp;price_min=&amp;price_max=',
                       url + '/category.php?id=191&amp;price_min=&amp;price_max=']
    # 这个for循环只处理了前两个一级目录，第三个里边只要两个二级目录
    for i in range(2):
        # 二级目录名及链接
        body = getHtml(first_grade_url[i])
        html = HtmlResponse(url=first_grade_url[i], body=str(body))
        soup = BeautifulSoup(body, 'lxml')
        # second_grade_name = soup.find_all()
        second_grade_name = []
        second_grade_url = []
        q = 1
        while(q):
            try:
                second_grade_name.append(html.xpath('/html/body/div[9]/div[2]/div[1]/dl/dd/ul/li[' + str(q) + ']/a/text()').extract()[0])
                second_grade_url.append(url + '/' + html.xpath('/html/body/div[9]/div[2]/div[1]/dl/dd/ul/li[' + str(q) + ']/a/@href').extract()[0])
                q += 1
            except:
                break
        # 在这个地方删掉不要的化工泵
        if second_grade_name[7] == u'\u5316\u5de5\u6cf5':
            del second_grade_name[7]
            del second_grade_url[7]
        for j in range(len(second_grade_name)):
            # 三级目录名及链接
            body =  getHtml(second_grade_url[j])
            html = HtmlResponse(url=second_grade_url[j], body=str(body))
            third_grade_name = []
            third_grade_url = []
            q = 1
            while(q):
                try:
                    third_grade_name.append(html.xpath('/html/body/div[9]/div[2]/div[1]/dl/dd/ul/li[' + str(q) + ']/a/text()').extract()[0])
                    # print(html.xpath('/html/body/div[9]/div[2]/div[1]/dl/dd/ul/li[' + str(q) + ']/a/text()').extract()[0])
                    third_grade_url.append(html.xpath('/html/body/div[9]/div[2]/div[1]/dl/dd/ul/li[' + str(q) + ']/a/@href').extract()[0])
                    # print(html.xpath('/html/body/div[9]/div[2]/div[1]/dl/dd/ul/li[' + str(q) + ']/a/@href').extract()[0])
                    url_data = defaultdict()
                    url_data['url'] = url + '/' + third_grade_url[q-1]  # 把主页url和解析到的按三级目录url片段拼起来
                    url_data['third_grade'] = third_grade_name[q-1]
                    url_data['second_grade'] = second_grade_name[j]
                    url_data['first_grade'] = first_grade_name[i]
                    url_data['created'] = int(time.time())
                    url_data['updated'] = int(time.time())
                    q += 1
                except:
                    break
    # 下面抓第三个一级目录下的两个二级目录下的三级目录
    second_grade_name = ['气体检测仪', '电力电工检测仪器']
    second_grade_url = ['http://www.sssmro.com/category.php?id=702&price_min=&price_max=',
                        'http://www.sssmro.com/category.php?id=722&price_min=&price_max=']
    for j in range(len(second_grade_name)):
        # 三级目录名及链接
        body = getHtml(second_grade_url[j])
        html = HtmlResponse(url=second_grade_url[j], body=str(body))
        third_grade_name = []
        third_grade_url = []
        q = 1
        while (q):
            try:
                third_grade_name.append(
                    html.xpath('/html/body/div[9]/div[2]/div[1]/dl/dd/ul/li[' + str(q) + ']/a/text()').extract()[0])
                # print(html.xpath('/html/body/div[9]/div[2]/div[1]/dl/dd/ul/li[' + str(q) + ']/a/text()').extract()[0])
                third_grade_url.append(
                    html.xpath('/html/body/div[9]/div[2]/div[1]/dl/dd/ul/li[' + str(q) + ']/a/@href').extract()[0])
                # print(html.xpath('/html/body/div[9]/div[2]/div[1]/dl/dd/ul/li[' + str(q) + ']/a/@href').extract()[0])
                url_data = defaultdict()
                url_data['url'] = url + '/' + third_grade_url[q - 1]  # 把主页url和解析到的按三级目录url片段拼起来
                url_data['third_grade'] = third_grade_name[q - 1]
                url_data['second_grade'] = second_grade_name[j]
                url_data['first_grade'] = first_grade_name[2]
                url_data['created'] = int(time.time())
                url_data['updated'] = int(time.time())
                q += 1
            except:
                break
    # 至此，所有的三级页面首页目录链接都存在了outline_data里
    return outline_data

def goodsUrlList(home_url):
    '''
    根据三级目录商品首页获取所有详情页url
    :param home_url: http://www.sssmro.com//category.php?id=1137&price_min=&price_max=
    :return:url列表
    '''
    # 该网站不需要条件选择即可抓到所有产品
    # 保存所有goods的详情页url
    url_list = []
    # 解析首页，拿到该三级目录下有几页网页
    body = getHtml(home_url)
    html = HtmlResponse(url=home_url, body=str(body))
    # 先拿到该三级目录下的产品有几页
    num = int(html.xpath('/html/body/div[9]/div[2]/div[4]/form/ul/li[1]/text()').extract()[0][2:])
    # 然后抓取每一页下的产品的url
    for i in range(1, num+1):
        iter_url = home_url + '&page=' + str(i) + '&sort=last_update&order=DESC'
        body = getHtml(iter_url)
        html = HtmlResponse(url=iter_url, body=str(body))
        alist = html.xpath('/html/body/div[9]/div[2]/form/div/div/div/p[1]/a/@href').extract()
        print(len(alist))
        for url in alist:
            url_list.append('http://www.sssmro.com//' + url + '|1')
    return url_list

def goodsDetail(detail_url):
    '''
    利用xpath解析关键字段
    :param detail_url: 详情页url
    :return: 因为每个详情页面可能会产生多条数据，所以返回值是一个以dict为元素的list，其中每一个dict是一条数据
    '''
    # 解析网页

    body = getHtmlByRequests(detail_url)
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
    url = 'http://mro.abiz.com/product/AB1000.htm'
    goodsDetail(url)