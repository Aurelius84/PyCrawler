# -*- coding:utf-8 -*-

"""
@version: 1.0
@author: kevin
@license: Apache Licence 
@contact: liujiezhang@bupt.edu.cn
@site: 
@software: PyCharm Community Edition
@file: ETL.py
@time: 16/11/24 下午4:31
"""
from dataBase.mysql import M
import time


class ETL(M):

    def __init__(self, db_name, table_name, data):
        if not (db_name and table_name):
            raise ValueError("db_name or table_name is empty!")
        M.__init__(self, db_name, table_name)
        self.db = db_name
        self.table = table_name
        self.data = data
        self.key_fields = ['price', 'name', 'pics', 'type',
                           'detail', 'source_url', 'storage', 'lack_period']
        self.key_type = [float, str, str, str, str, str, str, float]

    def run(self):
        # 检查数据类型合法性
        self.__setParamters()
        # 检查各个字段合法性
        self.__handleField()
        # 去除url重复
        self.__handleExist()
        # 去除价格/类型/名字重复
        self.__goodsExist()
        # 批量插入数据库
        # print(self.data)
        # exit()
        if self.data:
            M.insertAll(self,self.data)

    def __setParamters(self):
        '''
        检查整个数据类型是否合法
        :param data: 爬取数据 dict 或者 [dict,dict]
        :return: [dict,dict]
        '''
        # 必须非空
        if not self.data:
            raise ValueError('data is empty!')
        # 字典类型
        elif isinstance(self.data, dict):
            data_list = [self.data]
        # 列表嵌套字典类型
        elif isinstance(self.data, list) and isinstance(self.data[0], dict):
            data_list = self.data
        else:
            raise ValueError('data is illegal!')
        self.data = data_list
        return data_list

    def __handleField(self):
        '''
        校验各个字段是否合法
        :return:
        '''
        for _ in xrange(len(self.data)):
            one_data = self.data.pop(0)
            is_legal = True
            # 前五项是必备的
            for i in xrange(6):
                # 非空,且字段合法
                if (self.key_fields[i] not in one_data) or \
                        (not one_data[self.key_fields[i]]) or \
                        (not isinstance(one_data[self.key_fields[i]], self.key_type[i])):
                    is_legal = False
                    break
            # 记录创建时间
            if 'created' not in one_data:
                one_data['created'] = int(time.time())
            if 'updated' not in one_data:
                one_data['updated'] = int(time.time())
            if is_legal:
                self.data.append(one_data)
        return self.data

    def __handleExist(self):
        '''
        url去重
        :return:
        '''
        for _ in xrange(len(self.data)):
            one_data = self.data.pop(0)
            is_exist = False
            sql = "select source_url from {0} where source_url='{1}'  order by id limit 1".format(
                self.table, one_data['source_url'])
            # print(sql)
            is_exist = M.cursor(self).execute(sql)
            if not is_exist:
                self.data.append(one_data)
        return self.data

    def __goodsExist(self):
        '''
        相同产品去重
        :return:
        '''
        for _ in xrange(len(self.data)):
            one_data = self.data.pop(0)
            is_exist = False
            sql = "select id from {0} where price={1} and name='{2}' and type='{3}' order by id limit 1".format(
                self.table, one_data['price'], one_data['name'], one_data['type'])
            is_exist = M.cursor(self).execute(sql)
            if not is_exist:
                self.data.append(one_data)
        return self.data

if __name__ == '__main__':
    # self.key_fields = ['price', 'name', 'pics', 'type',
    #                        'detail', 'source_url', 'storage', 'lack_period']
    data = [{'price':10.4,'name':'风机','pics':'pic0|pic2','type':'封闭式','detail':'aaaa','source_url':'http://gaegagg.com'},\
            {'price':12.4,'name':'股风机','pics':'pic0|pic2','type':'封闭式','detail':'aaaa','source_url':'http://gaegagg.com'},\
            ]
    ETL('test','test',data).run()