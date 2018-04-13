#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/7# Copyright (c) 2018 spider3. All rights reserved.import requestsfrom lxml import etreeimport jsonfrom utils.get_baidu_coord import BaiduCoordfrom utils.get_address_by_ten_coord import get_address_by_ten_coordfrom utils.get_region_id import get_region_idfrom utils.save_pic import save_picclass Coomo_spider(object):    def __init__(self):        self.url = "https://www.coomo99.com/stores"        self.detail_urls = []        self.data = {"data": []}    def get_detail_page(self):        idnum = 71229        for detail_url in self.detail_urls:            html = requests.get(detail_url)            self.parse_detail(html.text, idnum)            idnum += 1    # 解析详情页    def parse_detail(self, html_text, idnum):        tmp = {}        html = etree.HTML(html_text)        nodes = html.xpath('//div[@class="col-md-6 store_show_map"]')[0]        name = nodes.xpath('./div[1]/h3/text()')[0]        phone_number = nodes.xpath('./div[2]/p[2]/text()')[0].split("：")[-1].strip()        address = nodes.xpath('./div[2]/p[3]/text()')[0].split("（")[0].split("：")[-1].strip()        bc = BaiduCoord(address.split(" ")[0])        print(address.split(" ")[0])        # try:        #     ten_coord = bc.get_ten_coord()        #     jw_coord = bc.get_jw_coord()        #     longitude = jw_coord["x"]        #     latitude = jw_coord["y"]        #        #     # 获取区信息,获取region_id_        #     region_data = get_address_by_ten_coord(x=ten_coord["x"], y=ten_coord["y"])        #     district = region_data['address_detail']['district']        #     regionid1, regionid2, regionid3 = get_region_id(district)        #        # except Exception as e:        #     regionid1, regionid2, regionid3 = 0, 0, 0        #     longitude = 0        #     latitude = 0        #     print(e)        #     print(address)        #     print(idnum)        # 进行图片下载        jw_coord = html.xpath('//div[@id="store_info"]/@data-store')[0]        json_coord = json.loads(jw_coord)        longitude = json_coord["longitude"]        latitude = json_coord["latitude"]        # print("经纬度：", jw_coord)        image_urls = html.xpath('//div[@class="store-images-thumbnail row"]/div/img/@src')        image_num = 1        shop_img = ""        if isinstance(image_urls, list):            for image_url in image_urls:                img_name = str(image_num) + ".jpg"                save_pic(image_url, "./shop-images/" + "1268/" + str(idnum), img_name)                shop_img += "shop-images/" + "1268/" + str(idnum) + "/" + img_name + ","                image_num += 1            shop_img = shop_img[:-1]        else:            shop_img = "brands_images/full/1268.png"        tmp["id"] = idnum        tmp["name"] = name        tmp["address"] = address        tmp["phone_number"] = phone_number        tmp["longitude"] = longitude        tmp["latitude"] = latitude        # tmp["region_id_1"] = regionid1        # tmp["region_id_2"] = regionid2        # tmp["region_id_3"] = regionid3        # tmp["data_source"] = 1        # tmp["create_time"] = "NOW()"        tmp["preview_image"] = shop_img        print(tmp)        self.data["data"].append(tmp)    # 解析页面，获取详细页的url,加入 self.detail_urls 列表    def parse_page(self, html_text):        html = etree.HTML(html_text)        nodes = html.xpath('//div[@class="row store-list"]')        for node in nodes:            href = node.xpath("./div[2]/div/div[1]/a/@href")[0]            baseurl = "https://www.coomo99.com"            href = baseurl + href            # print(href)            self.detail_urls.append(href)    # 输入页码返回内容    def get_html(self, page):        data = {"page": page}        response = requests.get(url=self.url, params=data)        return response.textdef main():    coo = Coomo_spider()    for i in range(1, 15):        html = coo.get_html(i)        print("正在获取：", i)        coo.parse_page(html)    coo.get_detail_page()    with open("../data/new_coomo3.json", "w") as f:        f.write(json.dumps(coo.data, ensure_ascii=False))if __name__ == '__main__':    main()