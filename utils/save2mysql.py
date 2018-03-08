#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/7# Copyright (c) 2018 spider3. All rights reserved.import pymysqldef save2mysql(host, user, password, db, tb, datas):    """    链接数据库，和数据，数据为字典格式，字段对应数据库字段    :param host: host    :param user: 用户名    :param password: 密码    :param db: 数据库    :param tb: 表    :param datas: 对应可迭代的字典格式的数据 [{},{},{}]    :return:    """    connection = pymysql.connect(host=host,                                 user=user,                                 password=password,                                 db=db,                                 port=3306,                                 charset='utf8')    with connection.cursor() as cursor:        datas = datas if isinstance(datas, list) else [datas]        # 查出表中所有字段的名字        search_sql = "select COLUMN_NAME,column_comment from INFORMATION_SCHEMA.Columns where table_name = '{}' and table_schema = '{}'".format(            tb, db)        cursor.execute(search_sql)        names_list_tupe = cursor.fetchall()        # 根据传入的字典数据过滤出字典中有的字段        names = [one_tuple[0] for one_tuple in names_list_tupe if one_tuple[0] in datas[0].keys()]        # names = list(filter(lambda x:x in {"name":"接电话","id":9999}.keys(),names))        print("names:", names)        # 根据字段和数据，插入数据        for data in datas:            insert_sql = insert_by_name(names, data, tb)            print(insert_sql)            cursor.execute(insert_sql)        connection.commit()def insert_by_name(names, data, tb):    """    根据输入表中数据的字段名字和每一条字典类型的数据，组成插入数据的mysql语句    :param names: 字段名字，可迭代对象    :param data: 对应字典格式一条数据    :param tb: 对应表格名字    :return: 对应插入sql语句    """    start_sql = "insert into {}(".format(tb)    end_sql = ") value("    for name in names:        start_sql += "`{}`,".format(name)        value = "'{}',".format(data[name].replace("'", "")) if isinstance(data[name], str) else "{},".format(data[name])        end_sql += value    # 要把最后的“,”去掉，否则sql语句报错    insert_sql = start_sql[:-1] + end_sql[:-1] + ")"    # 把 'NOW()' 改成  NOW()    insert_sql = insert_sql.replace("'NOW()'", "NOW()")    return insert_sqldef main():    data = {"id": 71413, "brand_id": 1320, "name": "'楷模大普（济宁红星美凯龙店）", "address": "济宁市红星美凯龙三楼西北角大普家具、拿铁家具、梵蒂尼软床",            "phone_number": "0537-5151332", "longitude": 116.60079762482256, "latitude": 35.40212166433135,            "region_id_1": "370000", "region_id_2": "370100", "region_id_3": "370103", "data_source": 1,            "create_time": "NOW()",            "preview_image": "shop-images/2003/71413/1.jpg,shop-images/2003/71413/2.jpg,shop-images/2003/71413/3.jpg,shop-images/2003/71413/4.jpg,shop-images/2003/71413/5.jpg"}    save2mysql("localhost", "root", "root", "my_test", "feigo_shops", data)if __name__ == '__main__':    main()