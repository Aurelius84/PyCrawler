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
import sys
import getopt
from mysql import M
from detail import *
#from dataMin.ETL import ETL

def parseOutline():
    '''
    解析类目函数入口
    :return: True or False
    '''
    url = 'http://www.runlian365.com/'
    try:
        # 实例化 表
        table_outline = M('runlian365','runlian365_outline')
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
    table_name = 'runlian365_outline'
    table_seed_name = 'runlian365_url'
    table_outline = M('spider',table_name)
    table_seed = M('spider',table_seed_name)
    # 查询所有url
    sql = 'select * from {0} order by id limit 10'.format(table_name)
    table_outline.cursor.execute(sql)
    outline_data = table_outline.cursor.fetchall()
    i = 0
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
            print seed_data['created']
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
    table_seed_name = 'runlian365_url'
    # 暂时存放到gov表
    table_gov_name = 'runlian365_gov'
    table_seed = M('spider',table_seed_name)
    table_gov = M('spider',table_gov_name)
    # 查询未入库种子
    sql = "select a.id,a.url from {0} a where a.url not in (select source_url from {1} order by id)  order by id".format(table_seed_name,table_gov_name)
    table_seed.cursor.execute(sql)
    seed_urls = table_seed.cursor.fetchall()
    # 抓取详情
    insert_data = []
    for seed in seed_urls:
        detail = goodsDetail(seed['url'])
        insert_data.append(detail)
    # 插入数据库
    table_gov.insertAll(insert_data)
    # 关闭数据库连接
    table_seed.close()
    table_gov.close()

def etl():
    site = 'runlian365'
    db_name = 'spider'
    # gov表
    gov_name = site + '_gov'
    table_gov = M(db_name,gov_name)
    # 每次处理量
    iter_count = 500
    sql = 'select * from {0} where is_contrast=0 order by id limit {1}'.format(gov_name,iter_count)
    n = table_gov.cursor.execute(sql)
    while n:
        datas = table_gov.cursor.fetchall()
        # ETL清洗
        ETL(db_name=db_name,site_name=site,data=datas).run()
        # 继续查库
        sql = 'select * from {0} where is_contrast=0 order by id limit {1}'.format(gov_name,iter_count)
        n = table_gov.cursor.execute(sql)
    print('ETL process is done!')
    # 关闭数据库
    table_gov.close()
    ETL.close()

def Usage():
    '''
    使用说明
    :return:
    '''
    print 'fetch.py usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '-o, --outline: parse outline and save into table_outline'
    print '-s, --seed: fetch seed url and insert into table_url'
    print '-d, --detail: parse detail and insert into table_gov'
    print '-e, --etl: clean data for table_gov and insert into table_detail'
def Version():
    '''
    版本号
    :return:
    '''
    print 'fetch.py 1.0.0'
def main(argv):
    '''
    程序主入口
    :param argv:终端参数
    :return:
    '''
    try:
        opts, args = getopt.getopt(argv[1:], 'hvo:', ['output=', 'foo=', 'fre='])
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif o in ('-v', '--version'):
            Version()
            sys.exit(0)
        elif o in ('-o', '--outline'):
            parseOutline()
            sys.exit(0)
        elif o in ('-s','--seed',):
            parseSeedUrl()
            sys.exit(0)
        elif o in ('-d','--detail',):
            parseDetail()
        elif o in ('-e','--etl',):
            etl()
        else:
            print 'unhandled option'
            sys.exit(3)

if __name__ == '__main__':
    #main(sys.argv)
    parseDetail()
