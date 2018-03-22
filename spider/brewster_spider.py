#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/22# Copyright (c) 2018 spider3. All rights reserved."""布鲁斯特""""""http://www.brewsterchina.com/Pages/select.aspx"""import json, timefrom selenium import webdriverfrom selenium.webdriver.common.by import Byfrom selenium.webdriver.support.ui import WebDriverWaitfrom selenium.webdriver.support import expected_conditions as ECfrom selenium.webdriver.support.select import Selectdriver = webdriver.Chrome()url = 'http://www.brewsterchina.com/Pages/select.aspx'driver.get(url)def get_data(num):    try:  # 等待选择省份        element = WebDriverWait(driver, 10).until(            EC.presence_of_element_located((By.CLASS_NAME, "selectDiv"))        )        print("get_it")    except:        pass    # 修改省下拉为display    js = 'document.getElementsByClassName("selectDivList")[1].style.display="block";'    driver.execute_script(js)    sel = driver.find_element_by_class_name('selectDiv')    region = driver.find_element_by_xpath(        '//*[@id="ctl00"]/div[3]/div[2]/dl[2]/dd/div/div[2]/div/div[{}]'.format(num))  # 从第2到底35个    region.click()    driver.find_element_by_id('BtnSearch').click()    time.sleep(2)    nodes = driver.find_elements_by_xpath('//*[@id="UpdatePanel2"]/div[2]/ul/li')    li = []    for node in nodes:        tmp = {}        tmp["name"] = node.find_element_by_xpath('./p[2]').text        tmp["address"] = node.find_element_by_xpath('./p[3]').text        print(tmp)        li.append(tmp)    return lidef spider():    li = []    for num in range(2, 36):        li += get_data(num)    with open("../data/brewster.json", "w") as f:        f.write(json.dumps(li))def main():    spider()if __name__ == '__main__':    main()