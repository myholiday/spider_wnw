#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/26# Copyright (c) 2018 spider3. All rights reserved."""东鹏洁具""""""http://www.dongpengjieju.com/Brand/salenet.html"""import requestsimport jsonimport refrom lxml import etreefrom utils.add_detail import add_detail# 获取详情页地址def get_detail_urls(page):    url = 'http://www.dongpengjieju.com/Brand/salenet/p/{}.html'.format(page)    response = requests.get(url)    html = etree.HTML(response.text)    nodes = html.xpath('//tbody/tr/td[1]/a/@href')    detail_urls = ['http://www.dongpengjieju.com' + detail_url for detail_url in nodes]    print(detail_urls)    return detail_urls# 详细页def get_detail(detail_url):    response = requests.get(detail_url)    html = etree.HTML(response.text)    tmp = {}    tmp['name'] = html.xpath('//div[@class="news_detail_title"]/text()')[0]    tmp['address'] = html.xpath('//div[@class="news_detail_content"]/p[1]/text()')[0].replace('\xa0', '')    try:        jw = re.findall(r'BMap.Point\((.*?)\);', response.text)[0]        tmp['longitude'], tmp['latitude'] = jw.split(',')    except Exception as e:        pass    print(tmp)    return tmpdef spider():    li = []    detail_urls = []    for page in range(1, 15):        detail_urls += get_detail_urls(page)    for detail_url in detail_urls:        one_data = get_detail(detail_url)        li.append(one_data)    try:        with open('../data/dongpengjieju.json', 'w') as f:            f.write(json.dumps(li, ensure_ascii=False))    except Exception as e:        print(e)        with open('../data/dongpengjieju.json', 'w') as f:            f.write(json.dumps(li))def save():    add_detail(137631, 1435, '../data/dongpengjieju.json', '../data/dongpengjieju_detail.json')def main():    # spider()    save()if __name__ == '__main__':    main()