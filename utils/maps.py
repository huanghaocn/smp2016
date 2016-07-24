# -*- coding: utf-8 -*-

"""
@Time    : 16-7-22 下午5:26
@Author  : ino
@Site    : http://ino.design
@File    : maps.py
@notes   :
"""

# 将省份映射至地区编号
def province2Num(province):
    province2Num_dict = {
        2333:['None'],
        0:['辽宁','吉林','黑龙江'],
        1:['河北','山西','内蒙古','北京','天津'],
        2:['山东','江苏','安徽','浙江','台湾','福建','江西','上海'],
        3:['河南','湖北','湖南'],
        4:['广东','广西','海南','香港','澳门'],
        5:['云南','贵州','四川','西藏'],
        6:['新疆','陕西','宁夏','青海','甘肃'],
        7:[]
    }

    num = 999
    for subList in province2Num_dict.values():
        if (province in subList) | (len(subList)==0):
            num = province2Num_dict.keys()[province2Num_dict.values().index(subList)]
            break
    return num

# 将地区编号映射为地区中文
def num2Area(num):
    num2Area_dict = {
        0:'东北',
        1:'华北',
        2:'华东',
        3:'华中',
        4:'华南',
        5:'西南',
        6:'西北',
        7:'境外',
        2333:'None'
    }
    return num2Area_dict[num]

# 将名别映射为0|1
def gender2Flag(gender):
    gender2Flag_dict = {
        'f':0,
        'm':1,
        'None':2333
    }
    return gender2Flag_dict[gender]

# 将年龄段映射为0|1|2
def age2Flag(age):
    age2Flag_dict = {
        '-1979':0,
        '1980-1989':1,
        '1990+':2,
        'None':2333
    }
    if age<1980:
        return age2Flag_dict['-1979']
    elif (age>=1980) & (age<1990):
        return age2Flag_dict['1980-1989']
    else:
        return age2Flag_dict['1990+']

if __name__ == '__main__':
    print num2Area(province2Num('陕西'))

