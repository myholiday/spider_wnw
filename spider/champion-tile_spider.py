#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/19# Copyright (c) 2018 spider3. All rights reserved."""冠军瓷砖""""""http://www.champion-tile.com.cn/index.php/network"""import requestsfrom lxml import etreeimport jsonimport redef get_regions_id():    url = 'http://www.champion-tile.com.cn/index.php/network'    response = requests.get(url)    html = etree.HTML(response.text)    regions = html.xpath('//select[@id="sel_region"]/option/@value')    print(regions[1:])def get_citys_id(regions_id):    base_url = 'http://www.champion-tile.com.cn/index.php/dealer/change_resion/{}'    url = base_url.format(regions_id)    response = requests.get(url)    citys_id = re.findall("value='(.*?)'>",response.text)    return citys_iddef get_detail(city_id):    base_url = "http://www.champion-tile.com.cn/index.php/dealer/dealer_resion_map/{}/0/"    url = base_url.format(city_id)    response = requests.get(url)    data = json.loads(response.text)    data = data['data']    print(len(data))    return datadef add_name(data_li):    for data in data_li:        data["name"] = data['title']        data[""]def spider():    li = []    regions_id = get_regions_id()    for region_id in regions_id:  # 遍历省id        citys_id = get_citys_id(region_id)  # 得到市id        if citys_id:            for city_id in citys_id:  # 获取详细信息                data = get_detail(city_id)                li += datadef main():if __name__ == '__main__':    main()