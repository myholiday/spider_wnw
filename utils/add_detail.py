#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/16# Copyright (c) 2018 spider3. All rights reserved."""用来补充确实信息，一般官网只有门店地址，电话，名字"""import jsonfrom .get_baidu_coord import BaiduCoordfrom .get_address_by_ten_coord import get_address_by_ten_coordfrom .get_region_id import get_region_iddef add_detail(start_id, brand_id, old_dir, new_dir):    """    用来填充未完整的信息，并保存至new_dir    :param start_id: 开始id编号，查数据库得    :param brand_id: 品牌id    :param old_dir: 读取文件路劲及文件名    :param new_dir: 输出文件路劲及文件名    :return:    """    with open(old_dir, 'r') as f:        data = json.loads(f.read())    id = start_id    for one_data in data:  # 遍历每条数据，进行补充        one_data['id'] = id        id += 1        if 'phone_number' not in one_data or one_data['phone_number'] is None:  # 无phone_number字段也可以            one_data['phone_number'] = 0        if 'preview_image' not in one_data.keys():  # 没有自己维护图片时候自动维护            one_data['preview_image'] = 'brands_images/full/{}.jpg'.format(brand_id)        one_data['brand_id'] = brand_id        one_data['create_time'] = 'NOW()'        # 获取经纬度        try:            bc = BaiduCoord(one_data['address'])            if one_data['city']:  # 如果有地域限制                bc = BaiduCoord(one_data['address'], one_data['city'])            ten_coord = bc.get_ten_coord()            jw_coord = bc.get_jw_coord()            # 如果经纬度原来就有,则不添加            if 'longitude' not in one_data.keys() or 'latitude' not in one_data.keys():                one_data['longitude'] = jw_coord['x']                one_data['latitude'] = jw_coord['y']                one_data['official_coord'] = 0            else:  # 已经有地址，则维护字段official_coord，证明是在官网获取                one_data['official_coord'] = 1            if not bc.district:  # 如果高德api中没有记录到区信息，则到百度中获取                qu = get_address_by_ten_coord(ten_coord['x'], ten_coord['y'])                qu = qu['address_detail']['district']            if 'district' in one_data:  # 如果数据里面直接记录着区信息就用记录的                qu = one_data['district']            one_data['region_id_1'] = 0            one_data['region_id_2'] = 0            one_data['region_id_3'] = 0            try:                regionid1, regionid2, regionid3 = get_region_id(qu)                one_data['region_id_1'] = regionid1                one_data['region_id_2'] = regionid2                one_data['region_id_3'] = regionid3            except:                pass        except:            # 同上，如果经纬度原来就有,则不改为0            if 'longitude' not in one_data.keys() or 'latitude' not in one_data.keys():                one_data['longitude'] = 0                one_data['latitude'] = 0                one_data['official_coord'] = 0            else:  # 已经有地址，则维护字段official_coord，证明是在官网获取                one_data['official_coord'] = 1            one_data['region_id_1'] = 0            one_data['region_id_2'] = 0            one_data['region_id_3'] = 0            if 'district' in one_data:                qu = one_data['district']            try:                regionid1, regionid2, regionid3 = get_region_id(qu)                one_data['region_id_1'] = regionid1                one_data['region_id_2'] = regionid2                one_data['region_id_3'] = regionid3            except:                pass        print(one_data)    with open(new_dir, 'w') as f:        f.write(json.dumps(data))def main():    passif __name__ == '__main__':    main()