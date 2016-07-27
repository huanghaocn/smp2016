# -*- coding: utf-8 -*-

"""
@Time    : 16-7-25 下午2:06
@Author  : ino
@Site    : http://ino.design
@File    : jieba_tokenizer.py
@notes   :
"""
unlabeled_statuses_txt = '../../data/unlabeled_statuses.txt'
train_status_txt = '/home/shield/Competitions/smp-userProfile/train/train_status.txt'

import pandas as pd
import jieba
import time

def word_tokenizer():

    train_status_table = pd.read_table(unlabeled_statuses_txt,sep=',',index_col=False,header=None,names=['uid','n_retweet','n_review','source','time','content'])
    jieba.load_userdict('../dict_definited/street.txt')
    jieba.load_userdict('../dict_definited/xian_qu.txt')
    # jieba.load_userdict('../dict_definited/')
    # jieba.enable_parallel(4)
    with open('../output/tokenizer_result.txt','a+') as f:
        for sentence in train_status_table.content:
            seg_list = ' '.join(jieba.cut(sentence,HMM=True))
            seg = seg_list.encode("utf-8")+' ',
            f.writelines(seg)

def test():
    # jieba.load_userdict('../area_dict.txt')
    # jieba.load_userdict('../suyu_dict.txt')
    # sentence = '滚犊子宜家我就过去啦，冇催我,你老尾,陈紫琳'
    sentence = '姐妹们的聚会好嗨皮！还是怀念小时候，可以每天睡在一起聊天，到聊不动睡着。现在总是要在聊到最开心的时候说再见……'
    seg = jieba.cut(sentence=sentence,HMM=True)
    print ' '.join(seg)

if __name__ == '__main__':
    start = time.time()
    word_tokenizer()
    # test()
    end = time.time()
    print 'It costs %f seconds!!!'%(end-start)
