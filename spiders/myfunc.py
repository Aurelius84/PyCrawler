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

def getHtmlByVPN(url):
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

    table += u'''</tbody></table>'''

    return table

