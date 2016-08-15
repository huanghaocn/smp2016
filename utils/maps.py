# -*- coding: utf-8 -*-

"""
@Time    : 16-7-22 下午5:26
@Author  : ino
@Site    : http://ino.design
@File    : maps.py
@notes   :
"""

import pandas as pd
import os


# 将年龄段映射为0|1|2
def age2Flag(age):
    age2Flag_dict = {
        '-1979': 0,
        '1980-1989': 1,
        '1990+': 2,
        'None': 2333
    }
    if age < 1980:
        return age2Flag_dict['-1979']
    elif (age >= 1980) & (age < 1990):
        return age2Flag_dict['1980-1989']
    else:
        return age2Flag_dict['1990+']


# 将年龄段映射为0|1|2
def flag2Age(flag):
    flag2Age_dict = {
        0: '-1979',
        1: '1980-1989',
        2: '1990+',
    }
    return flag2Age_dict[flag]


# 将名别映射为0|1
def gender2Flag(gender):
    gender2Flag_dict = {
        'f': 0,
        'm': 1,
        'None': 2333
    }
    return gender2Flag_dict[gender]


# 将0|1映射为名别
def flag2Gender(flag):
    flag2Gender_dict = {
        0: 'f',
        1: 'm',
    }
    return flag2Gender_dict[flag]


# 将省份映射至地区编号
def province2Num(province):
    province2Num_dict = {
        2333: ['None'],
        0: ['辽宁', '吉林', '黑龙江'],
        1: ['河北', '山西', '内蒙古', '北京', '天津', '内蒙古自治区'],
        2: ['山东', '江苏', '安徽', '浙江', '台湾', '福建', '江西', '上海'],
        3: ['河南', '湖北', '湖南'],
        4: ['广东', '广西', '海南', '香港', '澳门', '广西壮族自治区'],
        5: ['云南', '贵州', '四川', '重庆', '西藏', '西藏自治区'],
        6: ['新疆', '陕西', '宁夏', '青海', '甘肃', '宁夏回族自治区', '新疆维吾尔自治区'],
        7: ['海外']
    }

    num = 2333
    for id in province2Num_dict:
        if (province in province2Num_dict[id]):
            num = id
            break

    return num


# 将地区编号映射为地区中文
def num2Area(num):
    num2Area_dict = {
        0: '东北',
        1: '华北',
        2: '华东',
        3: '华中',
        4: '华南',
        5: '西南',
        6: '西北',
        7: '境外',
        2333: 'None'
    }
    return num2Area_dict[num]


def resultEncoding(resultName, outputName):
    result_df = pd.read_csv(resultName, index_col=False, header=None, names=['uid', 'age', 'gender', 'province'])
    age = []
    gender = []
    province = []
    for row in range(len(result_df)):
        age.append(flag2Age(int(result_df.loc[row, 'age'])))
        gender.append(gender2Flag(int(result_df.loc[row, 'gender'])))
        province.append(num2Area(int(result_df.loc[row, 'province'])))
    temp_df = pd.DataFrame(columns=['uid', 'age', 'gender', 'province'])
    temp_df.uid = result_df.uid
    temp_df.age = age
    temp_df.gender = gender
    temp_df.province = province
    temp_df.to_csv(os.getcwd() + outputName, encoding='utf-8', index=False)


def province2area(province):
    north_east = [u'辽宁', u'吉林', u'黑龙江'],
    north = [u'河北', u'山西', u'内蒙古', u'北京', u'天津']
    east = [u'山东', u'江苏', u'安徽', u'浙江', u'台湾', u'福建', u'江西', u'上海']
    center = [u'河南', u'湖北', u'湖南']
    south = [u'广东', u'广西', u'海南', u'香港', u'澳门']
    south_west = [u'云南', u'贵州', u'四川', u'西藏', u'重庆']
    north_west = [u'新疆', u'陕西', u'宁夏', u'青海', u'甘肃']
    if province in north_east:
        location = u'东北'
    elif province in north:
        location = u'华北'
    elif province in east:
        location = u'华东'
    elif province in center:
        location = u'华中'
    elif province in south:
        location = u'华南'
    elif province in south_west:
        location = u'西南'
    elif province in south:
        location = u'华南'
    elif province in north_west:
        location = u'西北'
    else:
        location = u'境外'
    return location


def age2seg(age):
    if age < 1980:
        return '-1979'
    elif (age >= 1980) & (age < 1990):
        return '1980-1989'
    else:
        return '1990+'


if __name__ == '__main__':
    print num2Area(province2Num('None'))
    # resultEncoding()
