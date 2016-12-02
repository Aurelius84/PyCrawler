# -*- coding:utf-8 -*-

"""公共函数
@version: 1.0
@author: kevin
@license: Apache Licence
@contact: liujiezhang@bupt.edu.cn
@site:
@software: PyCharm Community Edition
@file: myfunc.py
@time: 16/11/25 上午10:45
"""
import urllib
import urllib2
from tornado_fetcher import Fetcher
import hashlib
import time
import requests
import random
from scrapy.http import HtmlResponse
import httplib
import socket
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    ]



def getHtmlByRequests(url):
    s = requests.session()
    user_agent = random.choice(user_agent_list)
    headers_base = {'Connection': 'keep=alive',
                    'Content-Encoding': 'gzip',
                    'Content - Language': 'zh - CN',
                    'Content - Type': 'text / html; charset = UTF - 8',
                    'Server': 'nginx',
                    'Set - Cookie': 'clientlanguage=zh_CN; path=/',
                    'Transfer - Encoding': 'chunked',
                    'User-Agent': user_agent,
                    'Referer': 'http://mro.abiz.com/',}
    response = s.get(url, headers=headers_base)
    return response.content


def getHtml(url,post_data=''):
    '''
    获取url对应Html内容
    :param url: 请求url
    :param post_data: post参数
    :return: html页面
    '''

    if post_data and isinstance(post_data,dict):
        data = urllib.urlencode(post_data)
        req = urllib2.Request(url,post_data=data)
    else:
        req = urllib2.Request(url)
    try:
        res = urllib2.urlopen(req).read()
        return res
    except Exception,e:
        print( Exception,":",e)

def getHtmlFromJs(url):
    '''
    获取js加载数据后的html
    :param url:请求url
    :return:
    '''
    fetcher=Fetcher(
          user_agent='phantomjs', # user agent
          phantomjs_proxy='http://localhost:4444', # phantomjs url
          pool_size=10, # max httpclient num
          async=False
          )
    return fetcher.phantomjs_fetch(url)

def getHtmlByVPN(url,headers=''):
    '''
    蚂蚁代理获取页面
    :param url:
    :return:
    '''

    #请替换appkey和secret
    appkey = "151161671"
    secret = "f7d28632cdf6ce18a2cb3672376d166d"
    paramMap = {
        "app_key": appkey,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")  #如果你的程序在国外，请进行时区处理
    }
    #排序
    keys = paramMap.keys()
    keys.sort()
    codes= "%s%s%s" % (secret,str().join('%s%s' % (key, paramMap[key]) for key in keys),secret)
    #计算签名
    sign = hashlib.md5(codes).hexdigest().upper()
    paramMap["sign"] = sign
    #拼装请求头Proxy-Authorization的值
    keys = paramMap.keys()
    authHeader = "MYH-AUTH-MD5 " + str('&').join('%s=%s' % (key, paramMap[key]) for key in keys)
    #接下来使用蚂蚁动态代理进行访问
    proxy_handler = urllib2.ProxyHandler({"http" : '123.56.92.151:8123'})
    opener = urllib2.build_opener(proxy_handler)
    # 伪装浏览器
    if headers:
        request = urllib2.Request(url,headers=headers)
    else:
        request = urllib2.Request(url)
    # 将authHeader放入请求头中即可,注意authHeader必须在每次请求时都重新计算，要不然会因为时间误差而认证失败
    request.add_header('Proxy-Authorization', authHeader)
    response = opener.open(request)
    return response.read()

def handleTable(table_name,table_param):
    '''
    格式化table
    :param table_name:参数名
    :param table_param:参数
    :return:table
    '''

    table = u'''<table border="1" cellpadding="0" cellspacing="0" width="100%"><tbody><tr><th colspan="2">产品参数</th></tr>'''

    for i in xrange(len(table_name)):
        line = u'''<tr><td class="name">{0}</td><td class="nr">{1}</td></tr>'''.format(table_name[i],table_param[i])
        table += line

    table += u'''</tbody></table><style>.default td{padding:2px 8px;border-right:1px solid #D8D8D8;border-bottom:1px solid #D8D8D8;}.default table{border-left:1px solid #D8D8D8;border-top:1px solid #D8D8D8;margin:10px 0}.default th{border-bottom:1px solid #D8D8D8;border-right:1px solid #D8D8D8;}.name{width:50%}</style>'''

    return table

def getProxyList():
    '''
    获取快代理的免费ip列表
    :return:
    '''
    import gzip
    from StringIO import StringIO
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        # 'Cache-Control':'max-age=0',
        # 'Connection':'keep-alive',
        # 'Cookie':'channelid=0; sid=1480509512181682; _ga=GA1.2.931640328.1480510967',
        'Host':'www.kuaidaili.com',
        'Referer':'http://www.kuaidaili.com/pricing/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'
    }
    total_page = 3
    ips = []
    ports = []
    for page in xrange(1,total_page+1):
        url = 'http://www.kuaidaili.com/proxylist/{0}'.format(page)
        req = urllib2.Request(url,headers=headers)
        buff = StringIO(urllib2.urlopen(req).read())
        f = gzip.GzipFile(fileobj=buff)
        body = f.read()
        html = HtmlResponse(url=url,body=body)
        cur_ips = html.selector.xpath('//*[@id="index_free_list"]/table/tbody/tr/td[1]/text()').extract()
        cur_ports = html.selector.xpath('//*[@id="index_free_list"]/table/tbody/tr/td[2]/text()').extract()
        types = html.selector.xpath('//*[@id="index_free_list"]/table/tbody/tr/td[3]/text()').extract()
        if cur_ips and len(cur_ips) == len(cur_ports):
            for i in xrange(len(cur_ips)):
                if types[i] == u'高匿名':
                    ips.append(cur_ips[i])
                    ports.append(cur_ports[i])
    return map(lambda ip,port:ip+':'+port,ips,ports)

def validateIp(ips):
    '''
    检测种子存活度
    :param ips:
    :return:
    '''
    url = "http://ip.chinaz.com/getip.aspx"
    socket.setdefaulttimeout(3)
    live_ips = []
    for i in xrange(len(ips)):
        try:
            proxy_host = "http://"+ips[i]
            proxy_temp = {"http":proxy_host}
            res = urllib.urlopen(url,proxies=proxy_temp).read()
            live_ips.append(ips[i])
            # if live_ips:
            #     break
            print ips[i]
            print(res)
        except Exception,e:
            print(ips[i],Exception,e)
    return live_ips

if __name__ == '__main__':
    ips = getProxyList()
    print(ips)
    print(validateIp(ips))