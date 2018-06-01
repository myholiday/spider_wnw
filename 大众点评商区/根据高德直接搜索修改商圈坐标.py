#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/5/30# Copyright (c) 2018 spider3. All rights reserved.import pymysqlimport requestsimport jsonimport timefrom retry import retrydef get_all_data():    connection = pymysql.connect(host='localhost',                                 user='root',                                 password='root',                                 db='qianxungou',                                 port=3306,                                 charset='utf8')    sql = "select `id`,`merger_name` from feigo_regions WHERE `level_type`=4 AND `short_name` is NULL; "    # 第三次开始    # 选择有 / 的跑一遍    # sql = "select `id`,`merger_name` from feigo_regions WHERE `level_type`=4 AND `short_name` is NULL AND `merger_name` LIKE '%/%'; "    # 第三次结束    with connection.cursor() as cursor:        cursor.execute(sql)        data = cursor.fetchall()    # print(data)    print(len(data))    return datadef get_coord_n_write_sql(data):  # 获取地名的,地址信息    address = data[1]    # 第三次    # 前    # address = address.split('/')[0]    # 后    # qian, hou = address.split('/')[:2]    # qian = qian.split(',')[:-1]+[hou]    # address = ",".join(qian)    # 第三次    address_last_name = address.split(",")[-1]  # 获取最后名字与高德返回数据做对比    address = ",".join(address.split(",")[2:])  # 只要市和区，搜索也准    print(address)    url = "http://restapi.amap.com/v3/place/text?key=5f2e9ed810bca7a99abc98f3808afce5&types=&city=&children=1&offset=20&page=1&extensions=all&keywords={}".format(address)    headers = {        'referer': 'https://ditu.amap.com/search?query=%E8%8F%9C%E5%B8%82%E5%8F%A3(%E5%9C%B0%E9%93%81%E7%AB%99)&city=440300&geoobj=113.935462%7C22.540659%7C113.940631%7C22.546719&zoom=17',        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'    }    try:        response = requests.get(url, headers=headers)    except:        time.sleep(1)        response = requests.get(url, headers=headers)    response = json.loads(response.text)    if "pois" not in response:  # 如果服务器出错        return    pois = response["pois"]    if not pois:  # 如果没找到        return    if len(pois) > 5:        pois = pois[:5]    # 检查前5个是否合格,合格则写入    for poi in pois:        if not poi["id"]:  # 如果id为空就跳过            continue        new_poi = get_detail_by_id(poi["id"])  # 返回的poi，为了防止高德返回错乱数据        amap_name = new_poi["name"]  # type: string        check_result = check_name_2(address_last_name, amap_name)        if check_result:            short_name = new_poi["name"]  # 用来存高德地图实际名字            lng, lat = new_poi["location"].split(",")            short_name = short_name.encode("utf-8").decode("utf-8")            f = open("第四次更新region经纬度.sql", "a", encoding="utf-8")            sql = "UPDATE `feigo_regions` SET `lng`={},`lat`={},`short_name`= '{}' WHERE `id`={};\n".format(lng, lat, short_name, data[0])            f.write(sql)            f.close()            print(sql)            returndef check_name_2(address_last_name, amap_name):    """    如果高德返回的名字都在    :param address_last_name:    :param amap_name:    :return:    """    strip_amap_name = amap_name.split("(")[0]  # 去掉括号防止公交站地铁站影响    if strip_amap_name in address_last_name:        return True  # 匹配成功    if "·" in strip_amap_name:        strip_amap_name = strip_amap_name.replace("·", "")        if strip_amap_name in address_last_name:            return True    if "政府" in strip_amap_name:        strip_amap_name = strip_amap_name[:-2]        if strip_amap_name in address_last_name:            return True    if strip_amap_name[-1] == "镇":        if strip_amap_name[:-1] in address_last_name:            return True    if strip_amap_name[-1] == "乡":        if strip_amap_name[:-1] in address_last_name:            return True    if strip_amap_name[-1] == "站":        if strip_amap_name[:-1] in address_last_name or strip_amap_name[:-1] in address_last_name.replace("省", "").replace("市", ""):            return True    if strip_amap_name in address_last_name:        return True  # 匹配成功    return Falsedef check_name(address_last_name, amap_name):    """    如果高德返回的名字里都在    :param address_last_name:    :param amap_name:    :return:    """    strip_amap_name = amap_name.split("(")[0]  # 去掉括号防止公交站地铁站影响    if strip_amap_name in address_last_name:        return True  # 匹配成功    return False@retry(10)def get_detail_by_id(amap_id):    """    根据amap_id返回 pois    :param amap_id:    :return: 返回 pois    """    url = "http://restapi.amap.com/v3/place/detail?key=5f2e9ed810bca7a99abc98f3808afce5&id={}".format(amap_id)    response = requests.get(url)    response = json.loads(response.text)    # print(url)    return response["pois"][0]def main():    data = get_all_data()    # print(data)    for one_data in data:        get_coord_n_write_sql(one_data)        print()    # ·    # get_coord_n_write_sql((522323008, '中国,贵州省,黔西南布依族苗族自治州,普安县,楼下镇'))if __name__ == '__main__':    main()