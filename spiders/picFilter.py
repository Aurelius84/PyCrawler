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
import shutil
'''
路径最好提前创建
防止识别出错
python 版本为 2.7
'''

# 数据路径
xls_path = u'D:\\git\\慧聪网图片地址3.xlsx'
# 图片保存文件夹路径
#pic_root = xls_path.split(u'.')[0]
pic_root = u'D:\\git\\test\\test'
# 文件名后缀
suffix = u'_filtered'
pic_root_filtered = str(pic_root) + str(suffix)
# 自动创建
#if not os.path.exists(pic_root):
#   os.mkdir(pic_root)

if not os.path.exists(pic_root_filtered):
    os.mkdir(pic_root_filtered)

# 加载数据
data = pd.read_excel(xls_path)
# 获取pics网址
pic_urls = set()
for i in xrange(len(data['pics'])):
    pics = str(data['pics'][i]).split(u'|')
    pic_urls |= set(pics)

if not pic_urls:
    exit("no pics need to download")

# 去除已经下载过的链接
sample = pic_urls.pop()
#print sample

pre_url = '/'.join(sample.split(u'/')[:-1])

# 检查当前路径下是否已经存在部分图片
exist_pics = set(os.listdir(pic_root))

N = len(pic_urls)
print('{0} pics need to fetch back....'.format(N))


# 判断是否需要加http
http_str = ''
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
        # 拷贝该文件到新文件夹下
        print token
        src_pic_path = os.path.join(pic_root,token)
        des_pic_path = os.path.join(pic_root_filtered,token)
        #print "src:" + src_pic_path
        #print "des:" + des_pic_path
        des_pic_path = os.path.join(pic_root_filtered,token)
        shutil.copy(src_pic_path, des_pic_path)
        print 'Pick {0} out '.format(token)
        continue

    pic_url = http_str + pic_url
    print pic_url
    continue
    # 图片后缀
    pic_name = pic_url.split(u'/')[-1]
    # 图片保存地址
    # 此处做了改动，存入新文件夹
    pic_path = pic_root_filtered + u'/' + pic_name

    pic_data = getHtmlByVPN(pic_url,http_type=http_type)
    # 保存图片
    f = open(pic_path,'wb')
    f.write(pic_data)
    f.close()
    print('save %s successfully'%pic_url)
    exit()
    if i%100==0:
        print('processing: %0.1f ....'%(float(i)/N))







