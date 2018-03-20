#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/20# Copyright (c) 2018 spider3. All rights reserved.import jsonimport reimport requestsfrom lxml import etreedef get_page(id):    li = []    url = 'http://www.yulanwallpaper.com.cn/getcities.aspx'    data = {'pg': 1, 'id': id}    response = requests.post(url, data)    total_page = int(response.text.split('||')[1])    if response.text.split('||')[0] == "true":        for i in range(1, total_page):            li += get_detail(i, id)    return lidef get_detail(pg, id):    li = []    url = 'http://www.yulanwallpaper.com.cn/getcities.aspx'    data = {'pg': pg, 'id': id}    response = requests.post(url, data)    messages = response.text.split('||')[-1]    html = etree.HTML(messages)    # names = html.xpath('//h3/text()')    names = re.findall(r'<h3>(.*?)</h3>', response.text)    # addresses = html.xpath('//p/text()')    addresses = re.findall(r'</strong>(.*?)</p>', response.text)    print(addresses)    if len(names) == len(addresses):        for i in range(len(names)):            tmp = {}            tmp['name'] = names[i]            tmp['address'] = addresses[i]            print(tmp)            li.append(tmp)    else:        print(id, pg)        raise EOFError        print()    return lidef spider():    li = []    for i in range(1, 33):  # 网页只有1-32        li += get_page(i)    with open('../data/yulan.json', 'w') as f:        f.write(json.dumps(li, ensure_ascii=False))def main():    spider()    # get_detail(1, 28)if __name__ == '__main__':    main()