# coding=utf-8
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.svm import SVC
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor
from sklearn.metrics import classification_report, mean_absolute_error
from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV
from sklearn.learning_curve import learning_curve
from utils import maps, preprocessor
import numpy as np
import json

if __name__ == '__main__':
    with open('data/train/train_info.txt') as info, open('data/train/train_labels.txt') as labels, \
            open('data/train/train_links.txt') as links, open('data/train/train_status.txt') as status, \
            open('data/other_links.txt') as other_links, open('data/unlabeled_statuses.txt') as ul_status, \
            open('data/test/test_info.txt') as test_info, open('data/test/test_status.txt') as test_status, \
            open('data/test/test_nolabels.txt') as test_no_labels, open(
            'nlp/dict_definited/areaDict_fullName2.json') as dict_d:
        # 读入训练集并进行预处理
        users = {}
        for line in info:
            uid = line.split('||')[0]
            users[uid] = {}
        for line in labels:
            infos = line.strip().split('||')
            uid = infos[0]
            users[uid] = {'content': ''}
            users[uid]['gender'] = infos[1]
            users[uid]['birthday'] = maps.age2seg(int(infos[2]))
            users[uid]['location'] = maps.province2area(infos[3].split(' ')[0].decode('utf-8'))
        for line in status:
            weibo = [t for t in line.strip().split(',')]
            uid = weibo[0]
            users[uid]['content'] += preprocessor.weibo_process(weibo[5]) + ' '
        # 读入测试集
        test_users = {}
        test_uid = []
        for line in test_no_labels:
            test_users[line.strip()] = {'content': ''}
            test_uid.append(line.strip())
        for line in test_status:
            weibo = [t for t in line.strip().split(',')]
            uid = weibo[0]
            if uid in test_users:
                test_users[uid]['content'] += preprocessor.weibo_process(weibo[5]) + ' '
        print 'data loaded'

        content, gender, birthday, location = [], [], [], []
        for uid in users:
            content.append(users[uid]['content'])
            gender.append(users[uid]['gender'])
            birthday.append(users[uid]['birthday'])
            location.append(users[uid]['location'])
        test_content = []
        for uid in test_uid:
            test_content.append(test_users[uid]['content'])

        area_dict = json.load(dict_d, 'utf-8')
        vectorizer = CountVectorizer(vocabulary=area_dict.keys())
        count_vector_train = vectorizer.fit_transform(content)
        count_vector_test = vectorizer.transform(test_content)

        # ch2_locatoin = SelectKBest(f_classif, k=600)
        # ch2_locatoin.fit(count_vector_train, location)
        # location_train = ch2_locatoin.transform(count_vector_train)
        # location_test = ch2_locatoin.transform(count_vector_test)
        location_train = count_vector_train
        location_test = count_vector_test
        # ch2_gender = SelectKBest(chi2, k=300)
        # ch2_gender.fit(count_vector_train, gender)
        # gender_train = ch2_gender.transform(count_vector_train)
        # gender_test = ch2_gender.transform(count_vector_test)
        gender_train = count_vector_train
        gender_test = count_vector_test

        # ch2_birthday = SelectKBest(f_classif, k=70)
        # ch2_birthday.fit(count_vector_train, birthday)
        # birthday_train = ch2_birthday.transform(count_vector_train)
        # birthday_test = ch2_birthday.transform(count_vector_test)
        birthday_train = count_vector_train
        birthday_test = count_vector_test
        # for feature in [vectorizer.get_feature_names()[i] for i in ch2_locatoin.get_support(indices=True)]:
        #     print feature

        clf = MultinomialNB()
        clf.fit(gender_train, gender)
        print classification_report(gender, clf.predict(gender_train))
        clf2 = MultinomialNB()
        clf2.fit(birthday_train, birthday)
        print classification_report(birthday, clf2.predict(birthday_train))
        # 用cross-validation寻找最优参数
        # clf3 = MultinomialNB(alpha=0.3)
        # tuned_params = [{'kernel': ['rbf'], 'C': [100, 300], 'gamma': [0.01, 0, 0.003]}]
        tuned_params = [{'alpha': [0.02, 0.05, 0.1]}]
        clf3 = GridSearchCV(MultinomialNB(), tuned_params, cv=5, n_jobs=-1)
        clf3.fit(location_train, location)
        clf3 = clf3.best_estimator_
        print classification_report(location, clf3.predict(location_train))
        gender_predict = clf.predict(gender_test)
        birthday_predict = clf2.predict(birthday_test)
        location_predict = clf3.predict(location_test)
        location_prob = clf3.predict_proba(location_test)
        location_prob = np.max(location_prob, axis=1)
        for i, uid in enumerate(test_uid):
            print '%s,%s,%s,%s,%f' % (
                uid, birthday_predict[i], gender_predict[i], location_predict[i], location_prob[i])
            # tuned_params = [{'alpha': [0.01, 0.03, 0.1, 0.3, 1.0], 'fit_prior': [True]},
            #                 {'alpha': [0.01, 0.03, 0.1, 0.3, 1.0], 'fit_prior': [False]}]
            # # tuned_params = [{'kernel': ['rbf'], 'C': [1, 10, 30, 60, 90], 'gamma': [0.1, 0.01, 0.001]}]
            # clf = GridSearchCV(MultinomialNB(), tuned_params, cv=3, verbose=3, n_jobs=-1)
            # clf.fit(location_train, location)
            # print clf.best_params_, clf.best_score_
            # train_size, train_scores, valid_scores = learning_curve(clf.best_estimator_, location_train, location,
            #                                                         train_sizes=[100 * (i + 1) for i in xrange(25)], cv=5)
            # print train_size
            # print np.mean(train_scores, 1)
            # print np.mean(valid_scores, 1)
