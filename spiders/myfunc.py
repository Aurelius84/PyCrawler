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
    print authHeader
    #接下来使用蚂蚁动态代理进行访问
    proxy_handler = urllib2.ProxyHandler({"http" : '123.56.92.151:8123'})
    opener = urllib2.build_opener(proxy_handler)
    request = urllib2.Request(url)
    # 将authHeader放入请求头中即可,注意authHeader必须在每次请求时都重新计算，要不然会因为时间误差而认证失败
    request.add_header('Proxy-Authorization', authHeader)
    response = opener.open(request)
    return response.read()


