# -*- coding: utf-8 -*-

"""
@Time    : 16-8-2 下午2:25
@Author  : ino
@Site    : http://ino.design
@File    : tags_search.py
@notes   :
"""

import pandas as pd
import numpy as np
import jieba
import jieba.analyse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import re
import types
import time

train_status_txt = '/home/shield/Competitions/smp-userProfile/train/train_status.txt'
train_label_txt = '../../data-normalized/label_maps.csv'

valid_status_txt = '/home/shield/Competitions/smp-userProfile/validation/test_status.txt'
valid_nolabel_txt = '/home/shield/Competitions/smp-userProfile/validation/test_nolabels.txt'


def areaTags_extraction(topk=30):
    '''
    DESCRIPTION: statistic the classic TAGS for each area by using tf-idf & removed intersection TAGS
    '''
    train_status_table = pd.read_table(train_status_txt,sep=',',index_col=False,header=None,names=['uid','n_retweet','n_review','source','time','content'])
    train_label_table = pd.read_csv(train_label_txt)

    areaTags_mat = []
    areaTagsANDWeight_mat = []

    for area in set(train_label_table.area.values.tolist()):
        # if area < 6:continue
        '''
        TODO;
        let each of weibo be a document
        '''
        corpus = []
        for uid in train_label_table[train_label_table.area==area].uid.values.tolist():
            content = ''
            for weibo in train_status_table[train_status_table.uid==uid].content.values.tolist():
                if type(weibo) == type(0.1):continue
                content += weibo
            corpus.append(content)

        vectorizer = CountVectorizer()
        wordsCount = vectorizer.fit_transform(corpus)
        # print wordsCount.toarray()

        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(wordsCount)

        tags_list = vectorizer.get_feature_names()
        areaTags_mat.append(tags_list)

        content_weight = tfidf.toarray()
        tag_weight = content_weight.sum(axis=0)
        tagsANDWeight_dict = dict([tags_list[i],tag_weight[i]] for i in range(len(tag_weight)))
        areaTagsANDWeight_mat.append(tagsANDWeight_dict)
        
        # if area>=1:
        #     break

    cols = ['area']
    cols.extend(['Tags_'+str(index+1) for index in range(topk)])
    train_areaTags_df = pd.DataFrame(columns=cols)

    '''
    removed_list will be used when extract tags of testing dataSet
    '''
    removed_list = []
    for i in range(len(areaTags_mat)):
        tmp = []
        for j in range(len(areaTags_mat)):
            if not i == j:
                tmp.extend(areaTags_mat[j])
        # delele intersection tags
        removed_list.extend(list(set(areaTags_mat[i]).intersection(set(tmp))))
        for tag in list(set(areaTags_mat[i]).intersection(set(tmp))):
            del areaTagsANDWeight_mat[i][tag]
        for tag in areaTagsANDWeight_mat[i].keys():
            if re.findall(r"[\w|\d]",tag):
                del areaTagsANDWeight_mat[i][tag]
        sorted_tagsWeight_dict = sorted(areaTagsANDWeight_mat[i].items(),key=lambda item:item[1],reverse=True)

        counter = 0
        row = [i]
        for k in sorted_tagsWeight_dict:
            if counter >= topk:
                break
            # print k[0],k[1]
            row.append(k[0])
            counter += 1
        # print row
        train_areaTags_df.loc[len(train_areaTags_df)] = row

    removed_list = list(set(removed_list))
    removed_df = pd.DataFrame(columns=['num','removed_tags'])
    removed_df.num = [i for i in range(len(removed_list))]
    removed_df.removed_tags = removed_list
    removed_df.to_csv('./removed_tags.csv',encoding='utf-8',index=False)
    # print removed_list
    # print train_areaTags_df
    train_areaTags_df.to_csv('./train_areaTags.csv',encoding='utf-8',index=False)

        # jieba.analyse.set_stop_words('../dict_definited/stopWords.txt')
        # tags = jieba.analyse.extract_tags(content, topK=20)
        # print area,(" ".join(tags))
    

def uid_tags(topk=10):
    valid_status_table = pd.read_table(valid_status_txt,sep=',',index_col=False,header=None,names=['uid','n_retweet','n_review','source','time','content'])
    valid_nolabel_table = pd.read_table(valid_nolabel_txt,index_col=False,header=None,names=['uid'])

    userTags_dict = {}
    userTagsANDWeight_dict = {}
    for uid in set(valid_nolabel_table.uid.values.tolist()):
        corpus = []
        for weibo in valid_status_table[valid_status_table.uid==uid].content.values.tolist():
            if type(weibo) == type(0.1):continue
            corpus.append(weibo)
            
        vectorizer = CountVectorizer()
        wordsCount = vectorizer.fit_transform(corpus)

        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(wordsCount)

        tags_list = vectorizer.get_feature_names()
        userTags_dict[uid] = tags_list
        
        content_weight = tfidf.toarray()
        tags_weight = content_weight.sum(axis=0)
        
        tagsANDWeight_dict = dict([tags_list[i],tags_weight[i]] for i in range(len(tags_list)))
        userTagsANDWeight_dict[uid] = tagsANDWeight_dict

        # break

    removed_df = pd.read_csv('./removed_tags.csv')

    cols = ['uid']
    cols.extend(['Tags_'+str(index+1) for index in range(topk)])
    test_tags_df = pd.DataFrame(columns=cols)
    uidOutOf_list = []

    for uid_key in userTagsANDWeight_dict.keys():
        # print uid_key
        for tagANDWeight in userTagsANDWeight_dict[uid_key].items():
            # print tagANDWeight
            if (tagANDWeight[0].encode('utf-8') in removed_df.removed_tags.values.tolist()) or (re.findall(r"[\w|\d]",tagANDWeight[0].encode('utf-8'))):
                del userTagsANDWeight_dict[uid_key][tagANDWeight[0]]
        sorted_userTagsANDWeight_dict = sorted(userTagsANDWeight_dict[uid_key].items(),key=lambda item:item[1],reverse=True)

        counter = 0
        row = [uid_key]
        for item in sorted_userTagsANDWeight_dict:
            if counter >= topk:break
            row.append(item[0])
            # print item[0],item[1]
            counter += 1
        if counter<topk:
            uidOutOf_list.append(uid_key)
            continue
        test_tags_df.loc[len(test_tags_df)] = row

    print 'uidOutOf_list',len(uidOutOf_list)
    print test_tags_df
    test_tags_df.to_csv('./test_tags.csv',encoding='utf-8',index=False)


if __name__ == '__main__':
    start = time.time()
    # areaTags_extraction(30)
    uid_tags()
    end = time.time()
    print 'It costs %f seconds!!!' % (end-start)