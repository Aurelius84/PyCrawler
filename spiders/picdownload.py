# -*- coding:utf-8 -*-

"""
@version: 1.0
@author: kevin
@license: Apache Licence 
@contact: liujiezhang@bupt.edu.cn
@site: 
@software: PyCharm Community Edition
@file: picdownload.py
@time: 16/11/30 下午3:01
"""
import pandas as pd
from time import time
import os
from myfunc import *
'''
路径最好提前创建
防止识别出错
python 版本为 2.7
'''

# 数据路径
xls_path = u'/Users/Kevin/Desktop/数据/sssmro网站数据.xls'
# 图片保存文件夹路径
pic_root = xls_path.split(u'.')[0]

# 自动创建
if not os.path.exists(pic_root):
    os.mkdir(pic_root)

# 加载数据
data = pd.read_excel(xls_path)
# 获取pics网址
pic_urls = set()
for i in xrange(len(data['pics'])):
    pics = data['pics'][i].split(u'|')
    pic_urls |= set(pics)

if not pic_urls:
    exit("no pics need to download")

# 去除已经下载过的链接
sample = pic_urls.pop()
pre_url = '/'.join(sample.split(u'/')[:-1])

# 检查当前路径下是否已经存在部分图片
exist_pics = set(os.listdir(pic_root))

N = len(pic_urls)
print('{0} pics need to download....'.format(N))

# 判断是否需要加http
http_type = u'http'
if sample.find(u'http') == -1:
    http_str = http_type +'://'

# 下载图片
pic_urls = list(pic_urls)

for i in xrange(N):
    # 图片地址
    pic_url = pic_urls.pop(0)

    # 判断是否下载过
    token = pic_url.split('/')[-1]
    if token in exist_pics:
        continue

    pic_url = http_str + pic_url
    # 图片后缀
    pic_name = pic_url.split(u'/')[-1]
    # 图片保存地址
    pic_path = pic_root + u'/' + pic_name

    pic_data = getHtmlByVPN(pic_url,http_type=http_type)
    # 保存图片
    f = open(pic_path,'wb')
    f.write(pic_data)
    f.close()
    print('save %s successfully'%pic_url)
    if i%100==0:
        print('processing: %0.1f ....'%(float(i)/N))





