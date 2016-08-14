# -*- coding: utf-8 -*-

"""
@Time    : 16-7-20 下午7:49
@Author  : ino
@Site    : http://ino.design
@File    : data.py
@notes   :
    #1 when you run this file, copy all of the raw_data.txt into the `../raw-data`
"""

import pandas as pd
import sys
sys.path.append("..")
from utils.maps import *

'''
train_info_txt = '/home/shield/Competitions/smp-userProfile/train/train_info.txt'
train_label_txt = '/home/shield/Competitions/smp-userProfile/train/train_labels.txt'
train_status_txt = '/home/shield/Competitions/smp-userProfile/train/train_status.txt'
test_info_txt = '/home/shield/Competitions/smp-userProfile/test/test_info.txt'
test_nolabel_txt = '/home/shield/Competitions/smp-userProfile/test/test_nolabels.txt'
test_status_txt = '/home/shield/Competitions/smp-userProfile/test/test_status.txt'
'''

train_info_txt = '../data/train_info.txt'
train_label_txt = '/home/zeus/0or1/local-smp2016/data/train_labels.txt'
train_status_txt = '../data/train_status.txt'
test_info_txt = '../data/test_info.txt'
test_nolabel_txt = '../data/test_nolabels.txt'
test_status_txt = '../data/test_status.txt'

# 统计trainingSe、testingSet的 性别分布 | age分布 | area分布
def naiveStatistic():
    print '=== train ==='

    train_info_table = pd.read_table(train_info_txt,sep='\|\|',index_col=False,header=None,names=['uid','alias','url'],engine='python')
    train_label_table = pd.read_table(train_label_txt,sep='\|\|',index_col=False,header=None,names=['uid','gender','age','area'],engine='python')
    train_status_table = pd.read_table(train_status_txt,sep=',',index_col=False,header=None,names=['uid','n_retweet','n_review','source','time','content'])

    print 'n_train_info:',len(set(train_info_table.uid.values.tolist()))
    print 'n_train_label:',len(set(train_label_table.uid.values.tolist()))
    print 'n_train_status:',len(set(train_status_table.uid.values.tolist()))

    for uid in set(train_info_table.uid.values.tolist()):
        if uid not in set(train_label_table.uid.values.tolist()):
            print uid

    print '\n=== test ==='

    test_info_table = pd.read_table(test_info_txt,sep='\|\|',index_col=False,header=None,names=['uid','alias','url'],engine='python')
    test_nolabel_table = pd.read_table(test_nolabel_txt,index_col=False,header=None,names=['uid'])
    test_status_table = pd.read_table(test_status_txt,sep=',',index_col=False,header=None,names=['uid','n_retweet','n_review','source','time','content'])

    print 'n_test_info:',len(set(test_info_table.uid.values.tolist()))
    print 'n_test_nolabel:',len(set(test_nolabel_table.uid.values.tolist()))
    print 'n_test_status:',len(set(test_status_table.uid.values.tolist()))

    for uid in set(test_status_table.uid.values.tolist()):
        if uid not in set(test_nolabel_table.uid.values.tolist()):
            print uid
    '''
    2173436682
    1788888261
    1288547201
    2194658752
    1084548663
    1656221350
    1425708367
    '''

# label编码
def train_labelMap():
    print '=== train ==='
    train_label_table = pd.read_table(train_label_txt,sep='\|\|',index_col=False,header=None,names=['uid','gender','age','area'],engine='python')

    # print train_label_table
    n_female = len(train_label_table[train_label_table.gender=='f'])
    n_male = len(train_label_table[train_label_table.gender=='m'])
    n_others = len(train_label_table[(train_label_table.age<1980)])
    n_80s = len(train_label_table[(train_label_table.age>=1980)&(train_label_table.age<1990)])
    n_90s = len(train_label_table[(train_label_table.age>=1990)])
    stat_info = 'n_female,{0}\nn_male,{1}\nn_others,{2}\nn_80s,{3}\nn_90s,{4}'.format(n_female,n_male,n_others,n_80s,n_90s)

    prov_list = []
    for area in train_label_table.area.values.tolist():
        prov_list.append(area.split(' ')[0])

    train_label_table['prov'] = prov_list
    train_labelMap_table = pd.DataFrame(columns=['uid','gender','age','area'])
    for i in range(len(train_label_table)):
        row_list = [
            train_label_table.loc[i,'uid'],
            gender2Flag(train_label_table.loc[i,'gender']),
            age2Flag(train_label_table.loc[i,'age']),
            province2Num(train_label_table.loc[i,'prov'])
        ]
        train_labelMap_table.loc[i] = map(str,row_list)
    print train_labelMap_table
    train_labelMap_table.to_csv('./label_maps.csv',index=False,encoding='utf-8')

    # 取出none值
    # while 'None' in prov_list:
    #     prov_list.remove('None')
    prov_map_list = []
    # 对省份进行地区映射
    for prov in prov_list:
        prov_map_list.append(province2Num(prov))
    dicts = {}
    # 统计地区用户数
    for i in prov_map_list:
        if not dicts.has_key(i):
            dicts[i] = 1
        else:
            dicts[i] += 1
    stat_area = '东北,{0}\n华北,{1}\n华东,{2}\n华中,{3}\n华南,{4}\n西南,{5}\n西北,{6}\n境外,{7}\nNone,{8}' \
        .format(dicts.values()[0],dicts.values()[1],dicts.values()[2],dicts.values()[3],
        dicts.values()[4],dicts.values()[5],dicts.values()[6],dicts.values()[7],dicts.values()[8])

    with open('./train_stat.csv','w') as f:
        f.writelines('statItem,num\n')
        f.writelines(stat_info)
        f.writelines('\n')
        f.writelines(stat_area)


if __name__ == '__main__':
    train_labelMap()
