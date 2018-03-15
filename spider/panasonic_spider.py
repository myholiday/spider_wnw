#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/15# Copyright (c) 2018 spider3. All rights reserved.import jsonimport requestsfrom lxml import etree#  获取地址iddef get_areaids():    url = 'http://pro.panasonic.cn/service/introduce.html'    response = requests.get(url)    html = etree.HTML(response.text)    areaids = html.xpath('//select[@id="areaid"]')[0]    areaids = areaids.xpath('./option/@value')[1:]    print(areaids)    return areaids# 根据地址id获取门店li = []def get_data(areaid, page):    print("正在获取{}第{}页".format(areaid,page))    url = 'http://pro.panasonic.cn/service/saleNet.html'    page = page    data = {        'search_type': 0,        'cityid': 0,        'life_id': 0,        'areaid': areaid,        'page': page    }    response = requests.get(url, data)    if '没有找到您想要的结果' in response.text:        return data    page += 1    html = etree.HTML(response.text)    nodes = html.xpath('//table/tr')[1:]    for node in nodes:        tmp = {}        tmp["city"] = node.xpath('./td[1]/text()')[0]        tmp['name'] = node.xpath('./td[2]/text()')[0]        tmp['address'] = node.xpath('./td[3]/text()')[0]        try:            tmp['phone_number'] = node.xpath('./td[4]/text()')[0]        except:            tmp['phone_number'] = 0        li.append(tmp)    try:        arrow = html.xpath('//div[@class="hous_right l sv_sale"]/ul/li')[-1]    except:  # 没有翻页的页码也停        return    # 有东西就停    if arrow.xpath('./a/text()'):        return    get_data(areaid, page)def spider():    areaids = get_areaids()    for areaid in areaids:        get_data(areaid, 1)def save():    with open('../data/panasonic.json','w') as f:        f.write(json.dumps(li,ensure_ascii=False))def main():    spider()  # 爬取    save()  # 并保存原始数据if __name__ == '__main__':    main()