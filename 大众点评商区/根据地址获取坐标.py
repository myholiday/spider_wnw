#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/6/15# Copyright (c) 2018 spider3. All rights reserved.import requestsimport jsonfrom retry import retryfrom pymongo import MongoClientimport pymysqlconnection = pymysql.connect(host='localhost', user='root', password='root', db='qianxungou', port=3306, charset='utf8')name = "吉盛伟邦"def get_first_data(address):    url = "http://restapi.amap.com/v3/place/text?key=5f2e9ed810bca7a99abc98f3808afce5&types=&city=&children=1&offset=20&page=1&extensions=all&keywords={}".format(        address)    response = requests.get(url)    response = json.loads(response.text)    amap_id = response['pois'][0]['id'] if response["pois"][0]['id'] else response['pois'][1]['id']    poi = get_detail_by_id(amap_id)    print(poi)    return poi@retry(10)def get_detail_by_id(amap_id):    """    根据amap_id返回 pois    :param amap_id:    :return: 返回 pois    """    url = "http://restapi.amap.com/v3/place/detail?key=5f2e9ed810bca7a99abc98f3808afce5&id={}".format(amap_id)    response = requests.get(url)    response = json.loads(response.text)    print(url)    if "pois" not in response:        return    return response["pois"][0]def get_all_shanquan(qu_id):    """获取区对应所有商圈id"""    sql = "select `id`,`merger_name` from feigo_regions WHERE `level_type`=4 AND `parent_id`={} ; ".format(qu_id)    with connection.cursor() as cursor:        cursor.execute(sql)        data = cursor.fetchall()    print("DATA:", data)    return datadef write_sql(poi, address):    qu_id = poi["adcode"]    city_code = poi["citycode"]    qu_ids = get_all_shanquan(qu_id)  # 从数据库中获取对应    merger_name = name    lng, lat = poi["location"].split(",")    if len(qu_ids) == 0:        sanquan_id = int(qu_id) * 1000 + 1    else:        sanquan_id = qu_ids[-1][0] + 1        print(qu_ids)        tmp = qu_ids[0][1].split(",")[:-1]        tmp.append(name)        merger_name = ",".join(tmp)        print(tmp)    sql = "INSERT INTO `feigo_regions` (`id`,`name`,`parent_id`,`level_type`, `merger_name`, `lng`, `lat`) VALUES ({},'{}',{},4,'{}',{},{});  #  {}===={} \n".format(        sanquan_id, name, qu_id, merger_name, lng, lat, address, poi['name'])    print("SQL:", sql)    with open("./新增吉盛伟邦sql.sql", "a", encoding="utf-8") as f:        f.write(sql)def doit():    with open("./月星家居数据.json", "r", encoding="utf-8") as f:        data = f.read()        data = json.loads(data)        # print(data)        for one_data in data:            address = one_data["province"] + "," + one_data["city"] + "," + one_data["address"] + "," +name            poi = get_first_data(address)            write_sql(poi, address)            # breakdef doit2():    with open("./居然之家数据.json", "r") as f:        data = f.read()        data = json.loads(data)        # print(data)        for one_data in data:            address = one_data + "," + name if "居然" not in one_data else one_data            print("==============", address)            poi = get_first_data(address)            write_sql(poi, address)def doit3():    with open("./红星美凯龙数据.json", "r") as f:        data = f.read()        data = json.loads(data)        # print(data)        for one_data in data:            address = one_data["address"] + " " + name            print("address"+address)            poi = get_first_data(address)            write_sql(poi, address)            # breakdef doit4():    conn = MongoClient("localhost", 27017)    db = conn.amap_data    my_set = db.d9999    for poi in my_set.find():        write_sql(poi, poi['address'])def main():    # get_first_data("利通区利通南街东侧南一环南侧凯悦国际建材商贸城 月星家居")    # get_all_shanquan(341825)    doit4()if __name__ == '__main__':    main()