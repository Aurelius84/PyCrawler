# -*- coding:utf-8 -*-

"""
抓取主逻辑,分三个进程:解析三级目录,抓取种子,解析详情

@version: 1.0
@author: kevin
@license: Apache Licence 
@contact: liujiezhang@bupt.edu.cn
@site: 
@software: PyCharm Community Edition
@file: fetch.py
@time: 16/11/26 下午5:21
"""
from dataBase.mysql import M
from detail import *

def parseOutline():
    '''
    解析类目函数入口
    :return: True or False
    '''
    url = 'http://www.vipmro.com/'
    try:
        # 实例化 表
        table_outline = M('test','vipmro_outline')
    except Exception,e:
        print(Exception,":",e)
        return False
    # 抓取三级类目信息
    outline_data = goodsOutline(url)
    if not outline_data:
        print('Failed to parse outline, data is empty.')
        return False
    table_outline.insertAll(outline_data)
    print('Successfully parse outline data.')
    # 关闭数据库连接
    table_outline.close()
    return True

def parseSeedUrl():
    '''
    抓取种子入口
    :return:
    '''
    # 实例化 outline表
    table_name = 'vipmro_outline'
    table_seed_name = 'vipmro_url'
    table_outline = M('test',table_name)
    table_seed = M('test',table_seed_name)
    # 查询所有url
    sql = 'select * from {0} order by id limit 10'.format(table_name)
    table_outline.cursor.execute(sql)
    outline_data = table_outline.cursor.fetchall()
    for data in outline_data:
        # 获取种子url
        seed_urls = goodsUrlList(data['url'])
        if not seed_urls: # 为空,跳过
            continue
        # 插入数据列表
        insert_data = []
        for seed_url in seed_urls:
            # 先查询mysql中是否已经存在
            sql = "select id from {0} where url='{1}' order by id limit 1".format(table_seed_name,seed_url)
            is_exist = table_seed.cursor.execute(sql)
            if is_exist:
                continue
            seed_data = defaultdict()
            seed_data['url'] = seed_url
            seed_data['source_url'] = data['url']
            seed_data['first_grade'] = data['first_grade']
            seed_data['second_grade'] = data['second_grade']
            seed_data['third_grade'] = data['third_grade']
            seed_data['created'] = int(time.time())
            seed_data['updated'] = int(time.time())
            insert_data.append(seed_data)
        # 插入数据库
        table_seed.insertAll(insert_data)
    # 关闭数据库
    table_seed.close()
    table_outline.close()

def parseDetail():
    '''
    解析详情函数入口
    :return:
    '''
    table_seed_name = 'vipmro_url'
    table_detail_name = 'vipmro_detail'
    table_seed = M('test',table_seed_name)
    table_detail = M('test',table_detail_name)
    # 查询未入库种子
    sql = "select a.id,a.url from {0} a where a.url not in (select source_url from {1} order by id)  order by id".format(table_seed_name,table_detail_name)
    table_seed.cursor.execute(sql)
    seed_urls = table_seed.cursor.fetchall()
    # 抓取详情
    insert_data = []
    for seed in seed_urls:
        detail = goodsDetail(seed['url'])
        insert_data.append(detail)
    # 插入数据库
    table_detail.insertAll(insert_data)
    # 关闭数据库连接
    table_seed.close()
    table_detail.close()

if __name__ == '__main__':
    parseDetail()