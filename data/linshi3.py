#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/7# Copyright (c) 2018 spider3. All rights reserved.# todo 删除这个文件from utils.save2mysql import save2mysqlimport jsonfrom utils.save_pic import save_picdef get_img():    with open('../data/skyworth.json', 'r') as f:        li = json.loads(f.read())[-12:]    for one_data in li:        if one_data['img']:            img_name = one_data['preview_image'].split(',')            if len(img_name)!=len(one_data['img']):                print("+++++++++++++++++++++++++++++++", one_data)            for i in range(len(img_name)):                save_pic(one_data['img'][i], "F:/", img_name[i])                print("下载完成{}图片".format(img_name[i]))def main():    # spider()    get_img()if __name__ == '__main__':    main()