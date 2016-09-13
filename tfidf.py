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
import json

import pandas as pd


def predict_birthday(x_train, y_train, x_test):
    vectorizer = TfidfVectorizer(max_df=0.1)
    train_vector = vectorizer.fit_transform(x_train)
    test_vector = vectorizer.transform(x_test)
    tuned_params = [{'alpha': [0.001, 0.1, 1, 10]}]
    clf = GridSearchCV(MultinomialNB(), tuned_params, cv=5)
    clf.fit(train_vector, y_train)
    print clf.best_params_
    clf = clf.best_estimator_
    print classification_report(y_train, clf.predict(train_vector))
    return clf.predict(test_vector)


def predict_gender(x_train, y_train, x_test):
    vectorizer = TfidfVectorizer(max_features=1000)
    train_vector = vectorizer.fit_transform(x_train)
    test_vector = vectorizer.transform(x_test)
    tuned_params = [{'alpha': [0.001, 0.1, 1, 10]}]
    clf = GridSearchCV(MultinomialNB(), tuned_params, cv=5)
    clf.fit(train_vector, y_train)
    print clf.best_params_
    clf = clf.best_estimator_
    print classification_report(y_train, clf.predict(train_vector))
    return clf.predict(test_vector)


def predict_location(x_train, y_train, x_test):
    with open('nlp/dict_definited/locationFeatures.txt') as loc_features:
        area_set = set()
        for line in loc_features.readlines():
            if not line.startswith('#'):
                area_set.add(line.strip().decode('utf-8'))
        area_dict = [i for i in area_set]
    vectorizer = CountVectorizer(vocabulary=area_dict, analyzer='char', ngram_range=(1, 8))
    train_vector = vectorizer.fit_transform(x_train)
    test_vector = vectorizer.transform(x_test)
    tuned_params = [{'alpha': [0.001, 0.1, 1, 5, 10]}]
    clf = GridSearchCV(MultinomialNB(), tuned_params, cv=5)
    clf.fit(train_vector, y_train)
    print clf.best_params_
    clf = clf.best_estimator_
    print classification_report(y_train, clf.predict(train_vector))
    # for vec in test_vector:
    #     print json.dumps([vectorizer.get_feature_names()[j] for j in vec.indices],
    #                      ensure_ascii=False)
    return clf.predict(test_vector)


if __name__ == '__main__':
    with open('data/train/train_info.txt') as info, open('data/train/train_labels.txt') as labels, \
            open('data/train/train_links.txt') as links, open('data/train/train_status.txt') as status, \
            open('data/test/test_info.txt') as test_info, open('data/test/test_status.txt') as test_status, \
            open('data/test/test_nolabels.txt') as test_no_labels:
        # 读入训练集并进行预处理
        users = {}
        # for line in info:
        #     uid = line.split('||')[0]
        #     users[uid] = {}
        for line in labels:
            infos = line.strip().split('||')
            uid = infos[0]
            # if not maps.province2area(infos[3].split(' ')[0].decode('utf-8')) == u'境外':
            users[uid] = {'content': '', 'location_content': ''}
            users[uid]['gender'] = infos[1]
            users[uid]['birthday'] = maps.age2seg(int(infos[2]))
            users[uid]['location'] = maps.province2area(infos[3].split(' ')[0].decode('utf-8'))
            # if users[uid]['location'] != u'境外':
            #     users[uid]['location'] = u'境内'
        for line in status:
            weibo = [t for t in line.strip().split(',')]
            uid = weibo[0]
            if uid in users:
                if users[uid]['location'] != u'境外':
                    users[uid]['location_content'] += preprocessor.weibo_process(weibo[5], True)
                users[uid]['content'] += preprocessor.weibo_process(weibo[5], False)
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
                test_users[uid]['content'] += preprocessor.weibo_process(weibo[5], False)
                test_users[uid]['location_content'] += preprocessor.weibo_process(weibo[5], True)

        # 从info里获取性别
        gender_from_info = {}
        for line in test_info:
            infos = line.strip().split('||')
            uid = infos[0]
            gender = infos[2][-1:]
            if gender == '0':
                gender_from_info[uid] = 'f'
            elif gender == '1':
                gender_from_info[uid] = 'm'

        print 'data loaded'

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

        gender_predict = predict_gender(content, gender, test_content)
        birthday_predict = predict_birthday(content, birthday, test_content)
        location_predict = predict_location(location_content, location, location_test_content)
        # location_prob = clf3.predict_proba(location_test)
        # location_prob = np.max(location_prob, axis=1)
        temp_df = pd.DataFrame(columns=['uid', 'age', 'gender', 'province'])
        for i, uid in enumerate(test_uid):
            if uid in gender_from_info:
                gender = gender_from_info[uid]
            else:
                gender = gender_predict[i]
            print '%s,%s,%s,%s' % (
                uid, birthday_predict[i], gender, location_predict[i])

            temp_df.loc[len(temp_df)] = [uid, birthday_predict[i], gender, location_predict[i]]
        temp_df.to_csv('./temp_bayes.csv', index=False, encoding='utf-8')

            # uid, birthday_predict[i], gender, 'huibei')
            #     print location_prob[i]
            # print json.dumps([location.get_feature_names()[j] for j in birthday_test[i].indices],
            #                  ensure_ascii=False)

            # tuned_params = [{'alpha': [0.01, 0.03, 0.1, 0.3, 1.0], 'fit_prior': [True]},
            #                 {'alpha': [0.01, 0.03, 0.1, 0.3, 1.0], 'fit_prior': [False]}]
            # # tuned_params = [{'kernel': ['rbf'], 'C': [1, 10, 30, 60, 90], 'gamma': [0.1, 0.01, 0.001]}]
            # clf = GridSearchCV(MultinomialNB(), tuned_params, cv=3, verbose=3, n_jobs=-1)
            # clf.fit(location_train, location)
            # print clf.best_params_, clf.best_score_
            # train_size, train_scores, valid_scores = learning_curve(clf3, location_train, location,
            #                                                         train_sizes=[100 * (i + 1) for i in xrange(25)], cv=5)
            # print train_size
            # print np.mean(train_scores, 1)
            # print np.mean(valid_scores, 1)
