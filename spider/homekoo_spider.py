#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/23# Copyright (c) 2018 spider3. All rights reserved."""尚品宅配""""""http://www.homekoo.com/tiyandian/guangzhou"""from utils.add_detail import add_detailimport jsonfrom lxml import etreefrom selenium import webdriverfrom selenium import webdriverfrom selenium.webdriver.common.by import Byfrom selenium.webdriver.support.ui import WebDriverWaitfrom selenium.webdriver.support import expected_conditions as ECdriver = webdriver.Chrome()url = 'http://www.homekoo.com/tiyandian/guangzhou'driver.get(url)num = 1def get_region_urls():    try:  # 等待选择省份        element = WebDriverWait(driver, 10).until(            EC.presence_of_element_located((By.ID, "changeCity"))        )        print("get_it")    except:        print("没出现")    # # 修改省下拉为display    # js = 'document.getElementById("selectDivList")[1].style.display="block";'    # driver.execute_script(js)    region_url = driver.find_elements_by_xpath('//*[@id="changeCity"]/option')    region_urls = [i.get_attribute('value') for i in region_url]    return region_urls[1:]def get_detail(url):    global num    li = []    driver.get(url)    try:  # 等待选择省份        element = WebDriverWait(driver, 10).until(            EC.presence_of_element_located((By.ID, "changeCity"))        )        print("get_it")    except:        print("没出现")    store = driver.find_elements_by_class_name('store')    page_source = driver.page_source    html = etree.HTML(page_source)    nodes = html.xpath('//div[@class="store"]')    print(len(nodes))    for node in nodes:        tmp = {}        tmp["img"] = node.xpath('./div[1]/img/@src')[0]        tmp['address'] = node.xpath('./div[2]/p[2]/text()')[0]        tmp['name'] = node.xpath('./div[2]/h3/text()')[0]        tmp['preview_image'] = "shop-images/4825/{}.jpg".format(num)        num += 1        li.append(tmp)        print(tmp)    return lidef spider():    li = []    region_urls = get_region_urls()    print(region_urls)    for region_url in region_urls:        li += get_detail(region_url)    try:        with open("../data/homekoo.json", 'w') as f:            f.write(json.dumps(li, ensure_ascii=False))    except:        with open("../data/homekoo.json", 'w') as f:            f.write(json.dumps(li))def save():    add_detail(132625, 1204, '../data/homekoo.json', '../data/homekoo_detail.json')def main():    # spider()    save()if __name__ == '__main__':    main()