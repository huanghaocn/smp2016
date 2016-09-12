# -*- coding:utf-8 -*-

"""
@author: ino
@contact: ino.jonshoo@gmail.com
@site: http://ino.design
@file: age_model.py
@date: 16-9-11 下午8:33
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

import sys
sys.path.append('..')
from utils.maps import *

train_info_txt = '../data/train/train_info.txt'
train_label_map_txt = '../data-normalized/label_maps.csv'
train_label_txt = '../data/train/train_labels.txt'
train_status_txt = '../data/train/train_status.txt'
test_info_txt = '../data/test/test_info.txt'
test_nolabel_txt = '../data/test/test_nolabels.txt'
test_status_txt = '../data/test/test_status.txt'

def age_model(classifier='xgb'):
    # load train data
    train_info_table = pd.read_table(train_info_txt,sep='\|\|',index_col=False,header=None,names=['uid','alias','url'],engine='python')
    train_label_map_table = pd.read_csv(train_label_map_txt)
    train_label_table = pd.read_table(train_label_txt,sep='\|\|',index_col=False,header=None,names=['uid','gender','age','area'],engine='python')
    train_status_table = pd.read_table(train_status_txt,sep=',',index_col=False,header=None,names=['uid','n_retweet','n_review','source','time','content'])

    # load test data
    test_info_table = pd.read_table(test_info_txt,sep='\|\|',index_col=False,header=None,names=['uid','alias','url'],engine='python')
    test_nolabel_table = pd.read_table(test_nolabel_txt,index_col=False,header=None,names=['uid'])
    test_status_table = pd.read_table(test_status_txt,sep=',',index_col=False,header=None,names=['uid','n_retweet','n_review','source','time','content'])

    train_timestamp_df = timestamp_stat(train_status_table)
    test_timestamp_df = timestamp_stat(test_status_table)
    test_timestamp_df = pd.merge(test_nolabel_table,test_timestamp_df,on='uid',how='left')

    train_timestamp_xy = pd.merge(train_timestamp_df, train_label_map_table, on='uid', how='left')
    train_timestamp_y = train_timestamp_xy.age
    train_timestamp_x = train_timestamp_xy.drop(['uid','gender','age','area'], axis=1)

    test_uid = map(int,test_timestamp_df.uid.values.tolist())
    test_timestamp_x = test_timestamp_df.drop(['uid'],axis=1)

    birthday_predict = []

    if classifier == 'xgb':
        print '=== xgb training ==='
        clf = xgb.XGBClassifier(max_depth=3, learning_rate=0.005, n_estimators=50, silent=True,
                                 objective='binary:logistic', nthread=-1, gamma=0.3, min_child_weight=3,
                                 max_delta_step=0, subsample=0.8, colsample_bytree=1,
                                 colsample_bylevel=1.0,
                                 reg_alpha=0.1, reg_lambda=0.1, scale_pos_weight=1, base_score=0.5, seed=0,
                                 missing=None)
        clf.fit(train_timestamp_x, train_timestamp_y, sample_weight=None, eval_set=None, eval_metric=None,
                 early_stopping_rounds=None, verbose=True)
        print classification_report(train_timestamp_y, clf.predict(train_timestamp_x))

        birthday_predict = clf.predict(test_timestamp_x)

    elif classifier=='bayes':
        print '=== bayes training ==='
        clf = MultinomialNB()
        clf.fit(train_timestamp_x, train_timestamp_y)
        print classification_report(train_timestamp_y, clf.predict(train_timestamp_x))

        birthday_predict = clf.predict(test_timestamp_x)

    temp_df = pd.DataFrame(columns=['uid', 'age', 'gender', 'province'])
    temp_df.uid = test_uid
    age = []
    for i in birthday_predict:
        age.append(flag2Age(i))
    temp_df.age = age
    temp_df.gender = [flag2Gender(1) for j in range(len(test_uid))]
    temp_df.province = [num2Area(1) for k in range(len(test_uid))]

    # print temp_df
    temp_df.to_csv('./temp_age_xgb.csv', index=False, encoding='utf-8')


def timestamp_stat(df):
    cols = ['uid']
    cols.extend(map(str,range(24)))
    time_df = pd.DataFrame(columns=cols)
    uids = list(set(df.uid.values.tolist()))
    for uid in uids:
        dicts = dict([i,0] for i in range(24))
        row = [(int(uid))]
        for time in df[df.uid==uid].time.values.tolist():
            if len(time.split(' ')) == 2:
                timestamp = int(time.split(' ')[1].split(':')[0])
                dicts[timestamp] += 1
        row.extend(np.array(dicts.values())/float(sum(dicts.values())))
        time_df.loc[len(time_df)] = row

    return time_df

if __name__ == '__main__':
    age_model(classifier='xgb')