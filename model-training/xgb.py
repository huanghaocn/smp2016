# -*- coding:utf-8 -*-

"""
@author: ino
@contact: ino.jonshoo@gmail.com
@site: http://ino.design
@file: xgb.py
@date: 16-8-27 下午2:20
"""

import json
import time
import types
import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.grid_search import GridSearchCV
from sklearn.externals import joblib

import sys
sys.path.append('..')
from utils import maps, preprocessor

train_info_txt = '../data/train/train_info.txt'
train_label_map_txt = '../data-normalized/label_maps.csv'
train_label_txt = '../data/train/train_labels.txt'
train_status_txt = '../data/train/train_status.txt'
test_info_txt = '../data/test/test_info.txt'
test_nolabel_txt = '../data/test/test_nolabels.txt'
test_status_txt = '../data/test/test_status.txt'

def xgb_model():
    # load train data
    train_info_table = pd.read_table(train_info_txt,sep='\|\|',index_col=False,header=None,names=['uid','alias','url'],engine='python')
    train_label_map_table = pd.read_csv(train_label_map_txt)
    train_label_table = pd.read_table(train_label_txt,sep='\|\|',index_col=False,header=None,names=['uid','gender','age','area'],engine='python')
    train_status_table = pd.read_table(train_status_txt,sep=',',index_col=False,header=None,names=['uid','n_retweet','n_review','source','time','content'])

    # load test data
    test_info_table = pd.read_table(test_info_txt,sep='\|\|',index_col=False,header=None,names=['uid','alias','url'],engine='python')
    test_nolabel_table = pd.read_table(test_nolabel_txt,index_col=False,header=None,names=['uid'])
    test_status_table = pd.read_table(test_status_txt,sep=',',index_col=False,header=None,names=['uid','n_retweet','n_review','source','time','content'])

    # load dicts
    with open('../nlp/dict_definited/areaDict_fullName2.json') as dict_d:
        area_dict = json.load(dict_d, 'utf-8')

    source_df = pd.read_csv('../data-normalized/source.csv')
    source_sample = source_df.source.values.tolist()

    songs_d = []
    songs_f = open('../data-normalized/songs.txt', 'r')
    line = songs_f.readline()
    while line:
        songs_d.append(line.split(':')[0])
        line = songs_f.readline()

    movies_d = []
    movies_f = open('../data-normalized/movies.txt', 'r')
    line = movies_f.readline()
    while line:
        movies_d.append(line.split(':')[0])
        line = movies_f.readline()

    noutheast_dia = []
    noutheast_dia_f = open('../nlp/dict_definited/noutheast.txt', 'r')
    line = noutheast_dia_f.readline()
    while line:
        noutheast_dia.append(line.strip())
        line = noutheast_dia_f.readline()

    south_dia = []
    south_dia_f = open('../nlp/dict_definited/south.txt', 'r')
    line = south_dia_f.readline()
    while line:
        south_dia.append(line.strip())
        line = south_dia_f.readline()

    extent_data = []
    extent_data.extend(area_dict.keys())
    extent_data.extend(noutheast_dia)
    extent_data.extend(south_dia)
    extent_data = list(set(extent_data))

    train_uid = set(train_label_map_table.uid.values)
    test_uid = set(test_nolabel_table.uid.values)
    content, source, gender, birthday, location, test_content, test_source = [], [], [], [], [], [], []
    for uid in train_uid:
        if train_label_table[train_label_table.uid==uid].age.values[0]>2008 and \
                        train_label_table[train_label_table.uid == uid].age.values[0] < 1938:
            continue
        uid_content = ''
        for m in train_status_table[train_status_table.uid==uid].content.values:
            uid_content += ' ' + preprocessor.weibo_process(str(m).strip())
        content.append(uid_content)
        uid_source = ''
        for s in train_status_table[train_status_table.uid==uid].source.values:
            uid_source += ' ' + str(s).replace(' ', '').strip()
        source.append(uid_source)
        gender.append(train_label_map_table[train_label_map_table.uid==uid].gender.values[0])
        birthday.append(train_label_map_table[train_label_map_table.uid==uid].age.values[0])
        if train_label_map_table[train_label_map_table.uid==uid].area.values[0] == 8:
            location.append(loc_random())
        else:
            location.append(train_label_map_table[train_label_map_table.uid==uid].area.values[0])

    for uid in test_uid:
        uid_content = ''
        for m in test_status_table[test_status_table.uid == uid].content.values:
            uid_content += ' ' + preprocessor.weibo_process(str(m).strip())
        test_content.append(uid_content)
        uid_source = ''
        for s in train_status_table[train_status_table.uid == uid].source.values:
            uid_source += ' ' + s.replace(' ', '').strip()
        test_source.append(uid_source)

    gender_vectorizer = CountVectorizer(vocabulary=None)
    gender_train = gender_vectorizer.fit_transform(content)
    gender_test = gender_vectorizer.transform(test_content)

    birthday_vectorizer = CountVectorizer(vocabulary=None)
    birthday_train = birthday_vectorizer.fit_transform(content)
    birthday_test = birthday_vectorizer.transform(test_content)

    location_vectorizer = CountVectorizer(vocabulary=extent_data)
    location_train = location_vectorizer.fit_transform(content)
    location_test = location_vectorizer.transform(test_content)

    clf = MultinomialNB(class_prior=[2620, 780])
    clf.fit(gender_train, gender)
    print classification_report(gender, clf.predict(gender_train))

    clf2 = xgb.XGBClassifier(max_depth=5, learning_rate=0.03, n_estimators=180, silent=True,
                             objective='binary:logistic', nthread=-1, gamma=0.3, min_child_weight=3,
                             max_delta_step=0, subsample=0.8, colsample_bytree=0.5,
                             colsample_bylevel=1.0,
                             reg_alpha=0.3, reg_lambda=1.5, scale_pos_weight=1, base_score=0.5, seed=0,
                             missing=None)
    clf2.fit(birthday_train.toarray(), birthday, sample_weight=None, eval_set=None, eval_metric=None,
             early_stopping_rounds=None, verbose=True)
    print classification_report(birthday, clf2.predict(birthday_train.toarray()))
    joblib.dump(clf2, 'age_xgb.model')

    # clf3 = xgb.XGBClassifier(max_depth=7, learning_rate=0.2, n_estimators=175, silent=True,
    #                          objective='binary:logistic', nthread=-1, gamma=0.3, min_child_weight=2,
    #                          max_delta_step=0, subsample=0.8, colsample_bytree=0.6,
    #                          colsample_bylevel=0.6,reg_alpha=0.3, reg_lambda=1.0, scale_pos_weight=1,
    #                          base_score=0.3, seed=0,
    #                          missing=None)
    # clf3.fit(location_train.toarray(), location, sample_weight=None, eval_set=None, eval_metric=None,
    #          early_stopping_rounds=None, verbose=True)
    # print classification_report(location, clf3.predict(location_train.toarray()))

    tuned_params = [{'alpha': [0.1, 1, 5, 10]}]
    clf3 = GridSearchCV(MultinomialNB(), tuned_params, cv=5, n_jobs=-1)
    clf3.fit(location_train, location)
    clf3 = clf3.best_estimator_
    print classification_report(location, clf3.predict(location_train))

    gender_predict = clf.predict(gender_test)
    birthday_predict = clf2.predict(birthday_test.toarray())
    location_predict = clf3.predict(location_test.toarray())

    birthday_prob = clf2.predict_proba(birthday_test.toarray())

    location_prob = clf3.predict_proba(location_test.toarray())

    xgb_prob_df = pd.DataFrame(columns=['uid', 'age_0', 'age_1', 'age_2', 'loc_0', 'loc_1', 'loc_2', 'loc_3', 'loc_4', 'loc_5', 'loc_6', 'loc_7'])
    temp_df = pd.DataFrame(columns=['uid', 'age', 'gender', 'province'])
    for i, uid in enumerate(test_uid):
        tmp = [uid]
        tmp.extend(birthday_prob[i])
        tmp.extend(location_prob[i])
        xgb_prob_df.loc[len(xgb_prob_df)] = tmp

        temp_df.loc[len(temp_df)] = [str(int(uid)), maps.flag2Age(birthday_predict[i]), maps.flag2Gender(gender_predict[i]),
                                     maps.num2Area(location_predict[i])]
    xgb_prob_df.to_csv('./xgb_prob.csv', index=False, encoding='utf-8')
    temp_df.to_csv('./temp_xgb.csv', index=False, encoding='utf-8')

def loc_random():
    weight = [210,894,867,259,270,280,250,110]
    r = np.random.randint(0,sum(weight))
    for i,val in enumerate(weight):
        r -= val
        if r<0:
            return i

if __name__ == '__main__':
    start = time.time()
    xgb_model()
    end = time.time()
    print 'It costs %f seconds!!!' % (end-start)