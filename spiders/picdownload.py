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
import urllib
'''
路径最好提前创建
防止识别出错
python 版本为 2.7
'''

# 数据路径
xls_path = u'/Users/Kevin/Desktop/数据/sssmro网站数据.xls'
# 图片保存文件夹路径
pic_root = u'/Users/Kevin/Documents/'
# 加载数据
data = pd.read_excel(xls_path)
# 获取pics网址
pic_urls = set()
for i in xrange(len(data['pics'])):
    pics = data['pics'][i].split('|')
    pic_urls |= set(pics)
# 下载图片
for _ in xrange(len(pic_urls)):
    # 图片地址
    pic_url = pic_urls.pop()
    pic_url = 'http://www.sssmro.com/images/201510/goods_img/30419_P_1445996094879.jpg'
    # 图片后缀
    pic_name = pic_url.split('/')[-1]
    # 图片保存地址
    pic_path = pic_root + pic_name
    data = urllib.urlretrieve(pic_url,pic_path)
    print('save {0} successfully'.format(pic_path))






