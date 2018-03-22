#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/7# Copyright (c) 2018 spider3. All rights reserved.import requestsimport jsonclass BaiduCoord(object):    def __init__(self, address, city_or_region=None, use_amap_api=1):        """        根据地址，获取百度坐标        :param address: 输入地址        :param city_or_region: 是否有限制区域        :param amap_api: 是否用高德api进行地址定位        """        self.address = address        self.city = city_or_region if city_or_region else None        self.use_amap_api = use_amap_api        self.district = None    # 获取百度shi十字坐标    def get_ten_coord(self):        data = {"qt": "gc", "wd": self.address}        response = requests.get("http://api.map.baidu.com", params=data)        response_json = json.loads(response.text)        # print(response_json)        coord = response_json["content"]["coord"]        self.ten_coord = coord        return coord    # 根据百度十字坐标转换成经纬度坐标    def get_jw_coord(self):        # 高德api获取坐标，选取第一个，并将获取结果转成百度地图的经纬度        if self.use_amap_api:            url = 'http://restapi.amap.com/v3/place/text'            data = {'key': '5f2e9ed810bca7a99abc98f3808afce5', 'keywords': self.address, 'city': self.city,                    'children': 1, 'extensions': 'all'}            response = requests.get(url, data)            response_json = json.loads(response.text)            if response_json["status"] == '1' and response_json['count'] != '0':  # 成功                location = response_json['pois'][0]['location']  # 类似 "116.342873,39.846748"                self.district = response_json['pois'][0]['adname']  # 将高德地图获取的区信息绑定到district属性中                # 将高德坐标转成百度坐标                url2 = 'http://api.map.baidu.com/geoconv/v1/'                data2 = {"from": 3, "to": 5, "ak": "mDml72vqmPtHmZHl7tus153lx9e1pg8A", "coords": location}                response2 = requests.get(url2, data2)                response_json2 = json.loads(response2.text)                if response_json2["status"] == 0:                    return response_json2['result'][0]        # 百度api获取        if self.city:  # 如果有限制省市区            url = 'http://api.map.baidu.com/geocoder/v2/'            data = {"ak": "mDml72vqmPtHmZHl7tus153lx9e1pg8A", 'output': 'json', 'address': self.address,                    "city": self.city}            response = requests.get(url, params=data)            response_json = json.loads(response.text)            if response_json["status"] == 0:                location = response_json["result"]["location"]                return {'x': location['lng'], 'y': location['lat']}        else:  # 没有限制省市区            coord = self.ten_coord["x"] + "," + self.ten_coord["y"]            data = {"from": 6, "to": 5, "ak": "mDml72vqmPtHmZHl7tus153lx9e1pg8A", "coords": coord}            url = "http://api.map.baidu.com/geoconv/v1/"            response = requests.get(url, params=data)            response_json = json.loads(response.text)            if response_json["status"] == 0:                return response_json["result"][0]def main():    bc = BaiduCoord("北京市丰台区西四环南路红星美凯龙国际家居建材广场地下一层A8111", use_amap_api=0)    print(bc.get_ten_coord())    print(bc.get_jw_coord())if __name__ == '__main__':    main()