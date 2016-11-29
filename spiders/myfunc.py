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
import random

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

