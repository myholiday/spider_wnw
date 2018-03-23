#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/22# Copyright (c) 2018 spider3. All rights reserved."""创维""""""http://www.skyworth.com/shop/list/107"""import jsonimport requestsfrom lxml import etreefrom utils.save_pic import save_pici = 1def get_detail_url(page):    url = 'http://www.skyworth.com/shop/list/107?p={}'.format(page)    response = requests.get(url)    html = etree.HTML(response.text)    nodes = html.xpath('//*[@id="nrshow"]/div[1]/ul/li/a/@href')    li = []    for i in range(0, len(nodes), 2):        href = 'http://www.skyworth.com' + nodes[i]        li.append(href)        print(href)    return lidef parse_detail(url):    global i    tmp = {}    response = requests.get(url)    html = etree.HTML(response.text)    tmp['name'] = html.xpath('//div[@class="dmxx_1"]/p[2]/text()')[0].split('：')[-1]    tmp['address'] = html.xpath('//div[@class="dmxx_1"]/p[3]/text()')[0].split('：')[-1]    tmp['phone_number'] = html.xpath('//div[@class="dmxx_1"]/p[5]/text()')[0].split('：')[-1]    try:        tmp['img'] = ["http://www.skyworth.com" + i for i in html.xpath('//div[@class="dmxx_2"]/ul/strong/img/@src')]        if tmp['img']:            tmp['preview_image'] = 'shop-images/754/{}.jpg'.format(i)            i += 1        else:            raise Exception    except Exception as e:  # 无图片        print(e)        try:            imgs = ["http://www.skyworth.com" + i for i in html.xpath('//div[@class="dmxx_2"]/ul/img/@src')]            tmp['img'] = imgs            preview_image = ''            for _ in imgs:                if not preview_image:                    preview_image = 'shop-images/754/{}.jpg'.format(i)                    i += 1                else:                    preview_image += ',shop-images/754/{}.jpg'.format(i)                    i += 1            if preview_image:                tmp["preview_image"] = preview_image        except:            pass    print(tmp)    return tmpdef spider():    detail_href = []  # 用来记录详细页url    for page in range(1, 188):        detail_href += get_detail_url(page)    li = []    for detail_url in detail_href:        one_data = parse_detail(detail_url)        li.append(one_data)    try:        with open('../data/skyworth.json', 'w') as f:            f.write(json.dumps(li, ensure_ascii=False))    except Exception as e:        print(e)        with open('../data/skyworth.json', 'w') as f:            f.write(json.dumps(li))def get_img():    with open('../data/skyworth.json', 'r') as f:        li = json.loads(f.read())[215:500]  # todo 把这里去掉    for one_data in li:        if one_data['img']:            img_name = one_data['preview_image'].split(',')            if len(img_name)!=len(one_data['img']):                print("+++++++++++++++++++++++++++++++", one_data)            for i in range(len(img_name)):                save_pic(one_data['img'][i], "F:/", img_name[i])                print("下载完成{}图片".format(img_name[i]))def main():    # spider()    get_img()if __name__ == '__main__':    main()