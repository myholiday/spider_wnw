#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/5/29# Copyright (c) 2018 spider3. All rights reserved.import pymysqlimport requestsimport jsonimport timefrom retry import retrydef get_all_data():    connection = pymysql.connect(host='localhost',                                 user='root',                                 password='root',                                 db='feigo_data',                                 port=3306,                                 charset='utf8')    sql = "select `id`,`merger_name` from feigo_regions WHERE `level_type`=4; "    with connection.cursor() as cursor:        cursor.execute(sql)        data = cursor.fetchall()    # print(data)    print(len(data))    return data@retry(3)def get_jw_coord(data):    "5f2e9ed810bca7a99abc98f3808afce5"    address = data[1]    address = address.strip("其它")    address = address.replace("河南省,郑州市,其它商圈/区","河南省,郑州市,其它商圈/区")    url = "http://restapi.amap.com/v3/place/text?key=5f2e9ed810bca7a99abc98f3808afce5&types=&city=北京市&children=1&offset=20&page=1&extensions=all&keywords="+address    response = requests.get(url)    response = json.loads(response.text)  # type:dict    # print(response)    sql = "UPDATE `feigo_regions` SET `lng`=0,`lat`=0 WHERE `id`={};\n".format(data[0])    if "pois" not in response:  # 发生错误        return sql    pois = response["pois"]  # 没有数据    if len(pois) == 0:        return sql    count_lng, count_lat = 0, 0    pois_len = len(pois)    for one_data in pois:        lng, lat = one_data["location"].split(",")        count_lng += float(lng)        count_lat += float(lat)    lng = count_lng/pois_len    lat = count_lat/pois_len    print(lng, lat)    sql = "UPDATE `feigo_regions` SET `lng`={},`lat`={} WHERE `id`={};\n".format(lng, lat, data[0])    return sqldef compose_sql():    data = get_all_data()    data = data    for one_data in data:        print(one_data)        sql = get_jw_coord(one_data)        f = open("./change_regions_jw_sql.sql", "a")        f.write(sql)        f.close()        time.sleep(0.1)def main():    # get_all_data()    # get_jw_coord((654326006, '中国,天津,天津市,河西区,围堤道沿线'))    # get_jw_coord((654326006, '中国,河北省,保定市,清苑县,保定火车站东站'))    get_jw_coord((654326006, '中国,内蒙古自治区,乌兰察布市,察哈尔右翼中旗,巴音乡'))  # 113.0447203 41.2159    # compose_sql()if __name__ == '__main__':    main()