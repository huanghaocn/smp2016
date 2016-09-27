# coding=utf-8
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.svm import SVC, SVR
from sklearn.feature_selection import SelectKBest, chi2, f_classif, f_regression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor
from sklearn.metrics import classification_report, mean_absolute_error
from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV
from sklearn.learning_curve import learning_curve
from utils import maps, preprocessor
import numpy as np
from scipy.sparse import vstack
import json
import cPickle
import scipy.sparse
import pandas as pd


def predict_birthday(x_train, y_train, x_test):
    vectorizer = TfidfVectorizer(max_df=0.05, max_features=6000)
    train_vector = vectorizer.fit_transform(x_train)
    test_vector = vectorizer.transform(x_test)
    tuned_params = [{'alpha': [0.02, 0.05, 0.1]}]
    clf = GridSearchCV(MultinomialNB(), tuned_params, cv=5)
    clf.fit(train_vector, y_train)
    print clf.best_params_
    clf = clf.best_estimator_

    print classification_report(y_train, clf.predict(train_vector))
    return clf.predict(test_vector)


def predict_gender(x_train, y_train, x_test):
    vectorizer = TfidfVectorizer(max_df=0.1, max_features=13000)
    train_vector = vectorizer.fit_transform(x_train)
    test_vector = vectorizer.transform(x_test)
    tuned_params = [{'alpha': [0.001, 0.01, 0.07, 0.1, 1]}]
    clf = GridSearchCV(MultinomialNB(class_prior=[780, 2420]), tuned_params, cv=5, n_jobs=-1)
    clf.fit(train_vector, y_train)
    print clf.best_params_
    clf = clf.best_estimator_
    print classification_report(y_train, clf.predict(train_vector))
    return clf.predict(test_vector), clf.predict_proba(test_vector)


def predict_location(x_train, y_train, x_test, use_cache, print_learning_curve=False, predict_proba=False):
    if use_cache:
        with open('location_cache.pickle') as f:
            vectorizer, train_vector, test_vector, clf = cPickle.load(f)
    else:
        with open('location_cache.pickle', 'w') as f, \
                open('nlp/dict_definited/locationFeatures.txt') as loc_features:
            area_set = set()
            for line in loc_features.readlines():
                if not line.startswith('#'):
                    area_set.add(line.strip().decode('utf-8'))
            area_dict = [i for i in area_set]
            vectorizer = CountVectorizer(vocabulary=area_dict, analyzer='char', ngram_range=(1, 8))
            train_vector = vectorizer.fit_transform(x_train)
            test_vector = vectorizer.transform(x_test)
            tuned_params = [{'alpha': [0.8, 0.9, 1]}]
            clf = GridSearchCV(MultinomialNB(), tuned_params, cv=5)
            clf.fit(train_vector, y_train)
            print clf.best_params_
            clf = clf.best_estimator_
            cPickle.dump((vectorizer, train_vector, test_vector, clf), f)

    print classification_report(y_train, clf.predict(train_vector))
    if predict_proba:
        return clf.predict(test_vector), np.max(clf.predict_proba(test_vector), axis=1)
    else:
        return clf.predict(test_vector), test_vector


if __name__ == '__main__':
    with open('data/train/train_info.txt') as info, open('data/train/train_labels.txt') as labels, \
            open('data/train/train_links.txt') as links, open('data/train/train_status.txt') as status, \
            open('data/valid/valid_info.txt') as test_info, open('data/valid/valid_status.txt') as test_status, \
            open('data/valid/valid_nolabel.txt') as test_no_labels:
        # 读入训练集并进行预处理
        users = {}
        # for line in info:
        #     uid = line.split('||')[0]
        #     users[uid] = {}
        for line in labels:
            infos = line.strip().split('||')
            uid = infos[0]
            users[uid] = {'content': '', 'location_content': ''}
            users[uid]['gender'] = infos[1]
            users[uid]['birthday'] = maps.age2seg(int(infos[2]))
            users[uid]['location'] = maps.province2area(infos[3].split(' ')[0].decode('utf-8'))
        for line in status:
            weibo = [t for t in line.strip().split(',')]
            uid = weibo[0]
            if uid in users:
                if users[uid]['location'] != u'境外':
                    users[uid]['location_content'] += preprocessor.weibo_process(weibo[5], no_space=True)
                users[uid]['content'] += preprocessor.weibo_process(weibo[5], no_space=False)
        # 读入测试集
        test_users = {}
        test_uid = []
        for line in test_no_labels:
            test_users[line.strip()] = {'content': '', 'location_content': ''}
            test_uid.append(line.strip())
        for line in test_status:
            weibo = [t for t in line.strip().split(',')]
            uid = weibo[0]
            if uid in test_users:
                test_users[uid]['content'] += preprocessor.weibo_process(weibo[5], no_space=False)
                test_users[uid]['location_content'] += preprocessor.weibo_process(weibo[5],
                                                                                  no_space=True)

        location_content, content, gender, birthday, location = [], [], [], [], []
        for uid in users:
            if users[uid]['location_content']:
                location_content.append(users[uid]['location_content'])
                location.append(users[uid]['location'])
            content.append(users[uid]['content'])
            gender.append(users[uid]['gender'])
            birthday.append(users[uid]['birthday'])
        test_content, location_test_content = [], []
        for uid in test_uid:
            test_content.append(test_users[uid]['content'])
            location_test_content.append(test_users[uid]['location_content'])
        print 'data loaded'
        gender_predict, gender_prob = predict_gender(content, gender, test_content)
        birthday_predict = predict_birthday(content, birthday, test_content)
        location_predict, test_v = predict_location(location_content, location, location_test_content,
                                                    use_cache=False, print_learning_curve=False)
        for i, uid in enumerate(test_uid):
            print '%s,%s,%s,%s' % (
                uid, birthday_predict[i], gender_predict[i], location_predict[i])
