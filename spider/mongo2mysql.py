#!/usr/bin/env python# -*- coding: utf-8 -*-# Created by spider3 on 2018/3/28# Copyright (c) 2018 spider3. All rights reserved.import pymysqlimport requestsimport jsonimport osfrom retry import retryfrom requests.exceptions import ConnectionErrorfrom pymongo import MongoClientfrom utils.save_pic import save_picfrom utils.get_region_id import get_region_id, get_region_id_by_adcodefrom utils.save2mysql import save2mysqldef get_logo_pwd(brand_id):    """    输入brand_id,查询mysql中默认图片路径    :param brand_id:    :return:  默认图片路径    """    connection = pymysql.connect(host='localhost', user='root', password='root', db='qianxungou', port=3306, charset='utf8')    with connection.cursor() as cursor:        get_logo_sql = 'SELECT `logo` FROM `feigo_brands` WHERE `id`={}'.format(brand_id)        cursor.execute(get_logo_sql)        logo = cursor.fetchall()        print(logo[0][0])        return logo[0][0]# 默认set_name为brand_iddef mongo2mysql(start_id, set_name, brand_id=None):    """    将MongoDB的数据导入mysql    :param start_id:  起始id    :param set_name:   集合名字，一般设为brand_id    :param brand_id:   如果集合名字不是brand_id的时候，设置这个字段    :return:    """    if not brand_id:  # 如果没有输入brand_id则为数据集合名字        brand_id = int(set_name[1:])    start_id = start_id    conn = MongoClient('localhost', 27017)    db = conn.amap_data    my_set = eval('db.{}'.format(set_name))    all_data = list(my_set.find())    # 默认图片路径    # todo 可能没有logo_pwd    try:        logo_pwd = get_logo_pwd(brand_id)    except Exception as e:        logo_pwd = ""    # 记录amap_id    amap_ids = []    repeat_indexs = []  # 用于删除重复数据    # 遍历，添加详细信息    index = 0    for one_data in all_data:        # 如果已经储存，那么就不存这条数据了        if one_data['id'] in amap_ids:            repeat_indexs.append(index)            index += 1            continue        index += 1        amap_ids.append(one_data['id'])        one_data['amap_id'] = one_data['id']        one_data['id'] = start_id        start_id += 1        one_data['brand_id'] = brand_id        one_data['official_coord'] = 2  # 表示从高德爬取        one_data['create_time'] = 'NOW()'        one_data['address'] = one_data['address'] if one_data['address'] else " "        # 把电话号码中的'-'删除，用'/'代替';'隔开        one_data['phone_number'] = one_data['tel'].replace('-', '').replace(';', '/') if one_data['tel'] else ''        # 将高德经纬度转成百度经纬度        baidu_jw = jw_amap2baidu(one_data['location'])        one_data['longitude'], one_data['latitude'] = baidu_jw['x'], baidu_jw['y']        repeat_region_name = ['桥西区', '桥东区', '桥西区', '新华区', '城区', '矿区', '城区', '郊区', '城区', '和平区', '铁西区', '朝阳区', '铁西区', '铁东区', '向阳区', '郊区', '西安区', '宝山区', '鼓楼区', '通州区', '海州区', '清河区', '普陀区', '郊区', '鼓楼区', '西湖区', '市中区', '河东区', '鼓楼区', '新华区', '青山区', '永定区', '南山区', '城区', '江北区', '市中区', '市中区', '白云区', '新城区', '长安区', '城关区', '城中区', '新市区', '松山区', '大安区', '中山区', '大同区', '新兴区', '中正区', '中山区', '信义区', '东区', '南区', '西区', '大安区', '太平区', '和平区', '东区', '南区', '北区', '东山区', '新市区', '安定区', '东区', '北区', '东区', '西区', '泰山区', '金山区', '金门县', '连江县', '中西区', '东区', '南区', '北区', '地安门', '前门', '右安门', '首都机场', '天津站', '万新村', '太阳城', '华苑', '武清区', '宝坻区', '经济开发区', '静海县', '蓟县', '中山西路', '北正乡', '曹家渡', '大悦城', '世纪公园', '新街口地区', '大学城', '溧水区', '高淳区', '高新区', '经济技术开发区', '经济技术开发区', '开发区', '巴城镇', '其他地区', '沙溪镇', '陆渡镇', '经济开发区', '新天地', '四季青', '万达广场', '城西银泰', '永旺梦乐城', '金峰乡', '其他地区', '常安镇', '其他地区', '火车站', '万达广场', '西山', '大学城', '新桥', '洞头县', '永嘉县', '其他地区', '其他地区', '文成县', '泰顺县', '其他地区', '其他地区', '虹桥镇', '城隍庙', '凤凰城', '大学城', '南七里站', '矾山镇', '其他地区', '火车站', '大洋镇', '苏澳镇', '其他地区', '其他地区', '梅花镇', '南京西路', '中山路', '万达广场', '中山路', '火车站', '桃花镇', '辛家庵', '南京东路', '下罗', '火车站', '大上海城', '国贸', '紫荆山', '上街区', '北大学城', '升龙汇金广场', '高村乡', '高山镇', '城关镇', '城关乡', '新华路街道', '汉南区', '沌口', '经开万达', '江汉大学', '新洲区', '五一广场', '八一桥', '火车站', '汽车东站', '司门口', '解放西路', '王家湾', '开福寺', '高桥', '龙田镇', '其他地区', '官渡镇', '火车站', '城关镇', '东山镇', '城关镇', '龙门镇', '虹桥镇', '城关镇', '大荆镇', '沙溪镇', '城郊乡', '江南镇', '花桥镇', '城郊乡', '桥头乡', '万达广场', '大学城', '莲塘', '太阳城', '凤凰城', '火车站', '莲塘', '国贸', '万象城', '华侨城', '坪山', '龙华', '松岗', '凯德广场', '仲恺陈江', '沙田镇', '观音阁镇', '龙田镇', '龙潭镇', '龙华镇', '龙江镇', '凯德广场', '石碣镇', '茶山镇', '石排镇', '东坑镇', '麻涌镇', '沙田镇', '步行街', '人民公园', '会展中心', '万象城', '星光大道', '高新区', '火车站', '城厢镇', '城厢镇', '白山镇', '甘棠镇', '新圩镇', '石塘镇', '分水镇', '武陵镇', '溪口乡', '龙潭镇', '清溪镇', '大学城', '开发区', '大足区', '北部新区', '空港新城', '南桥寺', '黔江区', '新市镇', '官渡镇', '双凤镇', '太和镇', '板桥镇', '金龙镇', '白沙镇', '兴隆镇', '东城街道', '南城街道', '白羊镇', '高楼镇', '太平镇', '旧县镇', '双江镇', '太安镇', '清江镇', '福禄镇', '龙门镇', '大观镇', '竹山镇', '龙田乡', '龙河镇', '双龙镇', '永安镇', '高峰镇', '太平镇', '江口镇', '双河乡', '白云乡', '花桥镇', '三汇镇', '沙市镇', '江口镇', '双龙镇', '水口镇', '永安镇', '兴隆镇', '新民镇', '安坪镇', '福田镇', '龙溪镇', '双龙镇', '官渡镇', '铜鼓镇', '城厢镇', '凤凰镇', '马武镇', '沿溪镇', '龙沙镇', '三河镇', '桥头镇', '三星乡', '六塘乡', '龙潭乡', '官庄镇', '溪口镇', '大溪乡', '龙潭镇', '大溪镇', '兴隆镇', '板桥乡', '鹿角镇', '平安镇', '新田镇', '三义乡', '人民公园', '火车站', '李家沱', '人民北路', '高新区', '青白江区', '龙桥镇', '清流镇', '新民镇', '永宁镇', '三星镇', '清江镇', '三溪镇', '金龙镇', '土桥镇', '中和街道', '太平镇', '正兴镇', '大林镇', '永安镇', '黄水镇', '兴隆镇', '白沙镇', '三星镇', '古城镇', '上安镇', '寿安镇', '大兴镇', '复兴乡', '白云乡', '花桥镇', '兴义镇', '大观镇', '龙池镇', '中兴镇', '白鹿镇', '新兴镇', '邛崃市', '高新区', '五一路', '和谐世纪', '经开区', '大树营', '马街', '爱琴海购物公园', '万达广场', '龙城街道', '竹山镇', '嵩阳街道', '转龙镇', '九龙镇', '七星镇', '联合乡', '青龙街道', '火车站', '东大街', '莲湖公园', '安定门', '北大街', '西大街', '太华路沿线', '北关', '龙首原', '北大学城', '玉山镇', '三里镇', '三官庙镇', '金山镇', '草堂镇']        if one_data["adname"] in repeat_region_name:  # 如果实在重复的区里面,则用adcode获取区id            one_data['region_id_1'], one_data['region_id_2'], one_data['region_id_3'] = get_region_id_by_adcode(one_data["adcode"])        # 否则用区名字获取省市区信息        # 获取省市区        else:            one_data['region_id_1'], one_data['region_id_2'], one_data['region_id_3'] = get_region_id(one_data["adname"])        # if one_data['photos']:  # 如果有图片        #     # 用高德地图最后名字为图片名字        #     img_list = ['shop-images/{}/{}.jpg'.format(brand_id, url['url'].split('/')[-1].strip(".jpg")) for url in one_data['photos']]        #     one_data['preview_image'] = ",".join(img_list)        #     # 下载图片        #     for i in range(len(img_list)):        #         try:        #             save_pic(one_data['photos'][i]['url'], "F:\\", img_list[i])        #         except FileNotFoundError:  # 没有该文件夹,则创建对应brand_id的文件夹，然后再保存一次        #             os.makedirs('F:\\shop-images\\{}\\'.format(brand_id))        #             save_pic(one_data['photos'][i]['url'], "F:\\", img_list[i])        # else:  # 如果没有图片        #     one_data['preview_image'] = 'brands_images/full/{}.png'.format(brand_id)        one_data['preview_image'] = logo_pwd    # 删除重复数据    repeat_indexs.reverse()    for index in repeat_indexs:        del all_data[index]    print(len(all_data))    save2mysql("localhost", "root", "root", "my_test", "feigo_shops", all_data)    return start_id + 1  # 返回下次id@retry(ConnectionError, 4)def jw_amap2baidu(amap_jw):    """将高德地图经纬度转换成百度地图经纬度"""    url = 'http://api.map.baidu.com/geoconv/v1/'    data = {"from": 3, "to": 5, "ak": "mDml72vqmPtHmZHl7tus153lx9e1pg8A", "coords": amap_jw}    response = requests.get(url, data)    response_json = json.loads(response.text)    print(response_json['result'][0])    return response_json['result'][0]def main():    start_id = 470495    for set_id in range(9999, 10000):  # 上次到500 ；1420已入        set_id_str = 'd%.4d' % set_id        print(set_id_str, set_id)        try:            start_id = mongo2mysql(start_id, set_id_str, set_id)        except IndexError as e:            print("========%s=========" % set_id)            continue    # mongo2mysql(99999, "d0001", 1)    # get_region_id_by_adcode(410402)if __name__ == '__main__':    main()