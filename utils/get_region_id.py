#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/6# Copyright (c) 2018 spider3. All rights reserved.import pymysqldef get_region_id(qu):    """    输入区,如朝阳区,查询mysql表格，获得省、市、区编号    如果出错就返回三个 0    :param qu: 如 朝阳区    :return:    """    connection = pymysql.connect(host='localhost',                                 user='root',                                 password='root',                                 db='qianxungou',                                 port=3306,                                 charset='utf8')    regionid1, regionid2, regionid3 = 0, 0, 0    try:        with connection.cursor() as cursor:            sql = "select * from feigo_regions where `name`='{}'".format(qu)            cursor.execute(sql)            data = cursor.fetchall()            regionid3 = data[0][0]            regionid2 = data[0][2]            sql = "select * from feigo_regions where `id`=" + str(regionid2)            cursor.execute(sql)            data = cursor.fetchall()            regionid1 = data[0][2]    except Exception as e:        print(e)    finally:        return regionid1, regionid2, regionid3def main():    get_region_id('朝阳区')if __name__ == '__main__':    main()