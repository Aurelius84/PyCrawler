# -*- coding:utf-8 -*-

"""
@version: 1.0
@author: kevin
@license: Apache Licence 
@contact: liujiezhang@bupt.edu.cn
@site: 
@software: PyCharm Community Edition
@file: mysql.py
@time: 16/11/24 上午10:39
"""

import MySQLdb
import time


class DB(object):
    # 实例化数据库

    def __init__(self, db_name='test'):
        # 连接数据库
        self.connect = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='zlj521226',
            db=db_name,
            charset='utf8'
        )
        # 获取游标
        self.cursor = self.connect.cursor()

    def connect(self):
        '''
        复写connect方法
        :return:
        '''
        return self.connect

    def cursor(self):
        '''
        复写cursor方法
        :return:
        '''
        return self.cursor

    def close(self):
        '''
        关闭数据库
        :return:
        '''
        self.cursor.close()

    def commit(self):
        '''
        提交更改
        :return:
        '''
        self.connect.commit()

    def roolback(self):
        '''
        回滚
        :return:
        '''
        self.connect.rollback()


class M(DB):

    def __init__(self):
        # 继承DB类
        DB.__init__(self)

    def creatTable(self, args_dict):  # Todo 前期先在mysql手动建表
        '''
        创建数据表
        :param table_name: 表名
        :args_dict:字段名,类型 dict格式
        :return:
        '''
        pass

    def insertOne(self, table, data):
        if not isinstance(data, dict):
            raise KeyError("Insert data is not a dict")
        if not dict:
            raise ValueError("data is empty!")

        sql = "insert into {0}({1}) values({2})".format(
            table, ','.join(data.keys()), ','.join(['%s'] * len(data.keys())))
        param = tuple(data.values())
        # print(param)
        try:
            retrun_n = DB.cursor(self).execute(sql, param)
            DB.commit(self)
            print 'insert', retrun_n
        except KeyError:
            raise('Failed insert data.')
        DB.close(self)

if __name__ == '__main__':
    db_test = DB()
    table_test = M()

    data = {'id': 3, 'name': 'Ruler', 'create_time': '0987654321'}
    table_test.insertOne('test', data)
