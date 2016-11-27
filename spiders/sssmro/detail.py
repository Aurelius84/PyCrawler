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
        # soup = BeautifulSoup(body, 'lxml')
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
                    outline_data.append(url_data)
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
                outline_data.append(url_data)
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
    # 因为前面为了去重加了'|1'，现在要去除之
    detail_url = detail_url.split('|')[0]
    # 解析网页
    body = getHtml(detail_url)
    html = HtmlResponse(url=detail_url, body=str(body))

    # 根据页面中几个价格判断页面中有几个型号，然后创建几个dict
    sizes = html.xpath('//*[@id="relative_goods"]').extract()[0]    # //*[@id="relative_goods"]
    soup = BeautifulSoup(sizes, 'lxml')
    priceslist = soup.find_all('div', {'style': 'display:none;'})   # 存储包含有价格的html语句的list
    num = len(priceslist)   # num表示了该页面中有几个产品
    columnnum = len(soup.find('tr').find_all('td'))
    tmplist = soup.find_all('td')
    # 名称
    name = html.xpath('//*[@id="spec-list"]/ul/li/img/@alt').extract()[0]
    # 详情，包含两个标签，一个div，一个p，都是html语句，两个用换行符'\n'隔开
    detailInfo1 = html.xpath('//*[@id="sub11"]/div[1]').extract()[0]    # div
    try:
        detailInfo2 = html.selector.xpath('//*[@id="sub11"]/div[3]/p').extract()[0]   # p
    except:
        detailInfo2 = ''
    detailInfo = detailInfo1 + '\n' + detailInfo2
    # 图片
    # print(html.selector.xpath('//*[@id="spec-list"]/ul/li/img'))
    pics = []
    for pic in html.selector.xpath('//*[@id="spec-list"]/ul/li/img'):
        # 去除图片尺寸,方法图片('//*[@id="spec-n1"]/img')
        pics.append( 'www.sssmro/'+ pic.xpath('@src').extract()[0])
    pics = '|'.join(pics)
    goodslist = []
    for i in range(num):
        goodslist.append(defaultdict())
        goodslist[i]['price'] = float(priceslist[i].string.replace('\n\t\t\t   \n              ', '').replace(' \n              ', ''))
        goodslist[i]['type'] = tmplist[columnnum * (i + 1) + 1].string
        goodslist[i]['source_url'] = detail_url + '|' + str(i + 1)
        goodslist[i]['name'] = name
        goodslist[i]['detail'] = detailInfo
        goodslist[i]['pics'] = pics
        goodslist[i]['storage'] = ''
        goodslist[i]['lack_period'] = ''
        goodslist[i]['created'] = int(time.time())
        goodslist[i]['updated'] = int(time.time())
    return goodslist

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
    url = 'http://www.sssmro.com/goods.php?id=30419'
    llist = goodsDetail(url)
    for i in range(len(llist)):
        print(i, llist[i])
    print(len(llist))

    # 测试函数goodsOutline(url)
    # url = 'http://www.sssmro.com'
    # goodsOutline(url)

    # 测试函数goodsUrlList(home_url)
    # url = 'http://www.sssmro.com//category.php?id=1138&price_min=&price_max='
    # goodsUrlList(url)


