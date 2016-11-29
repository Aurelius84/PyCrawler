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

