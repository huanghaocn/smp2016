# -*- coding: utf-8 -*-

"""
@Time    : 16-7-22 下午4:31
@Author  : ino
@Site    : http://ino.design
@File    : test.py
@notes   :
    1. test file
"""
import pandas as pd

def province2Num(province):
    province2Num_dict = {
        0:['辽宁','吉林','黑龙江'],
        1:['河北','山西','内蒙古','北京','天津'],
        2:['山东','江苏','安徽','浙江','台湾','福建','江西','上海'],
        3:['河南','湖北','湖南'],
        4:['广东','广西','海南','香港','澳门'],
        5:['云南','贵州','四川','西藏'],
        6:['新疆','陕西','宁夏','青海','甘肃'],
        7:[]
    }

    num = 8
    for subList in province2Num_dict.values():
        if (province in subList) | (len(subList)==0):
            num = province2Num_dict.keys()[province2Num_dict.values().index(subList)]
            break
    return num

def num2Area(num):

    num2Area_dict = {
        0:'东北',
        1:'华北',
        2:'华东',
        3:'华中',
        4:'华南',
        5:'西南',
        6:'西北',
        7:'境外'
    }
    return num2Area_dict[num]

def mytest():
    df = pd.DataFrame({'a':[1,2,3],'b':[4,5,6]})
    # df = df.replace('None',-999).copy()
    df['C'] = [1,2,8]
    print df


if __name__ == '__main__':
    # print num2Area(province2Num('陕西'))
    a = [1,1,1,2,3,4]
    dicts = {}
    for i in a:
        if not dicts.has_key(i):
            dicts[i] = 1
        else:
            dicts[i] += 1
    print dicts.keys(),dicts.values()

    mytest()

    items = dict([('a',1),('b',2)])
    print items.keys()
    a = [1,2,3,3,4,4]
    print max(a)
    b = []

    df = pd.DataFrame({'a':[1,2,3],'b':[4,5,6]})
    print (df['b']-1)
    print df-1
