# -*- coding:utf-8 -*-

"""
@author: ino
@contact: ino.jonshoo@gmail.com
@site: http://ino.design
@file: result_ensemble.py
@date: 16-9-11 下午4:42
"""

import pandas as pd

bayes_csv = './20160911_067439.csv'
xgb_csv = '../model-training/temp_xgb.csv'

if __name__ == '__main__':
    bayes_df = pd.read_csv(bayes_csv)
    xgb_df = pd.read_csv(xgb_csv)

    merge_df = pd.merge(bayes_df,xgb_df,on='uid')
    temp_df = pd.DataFrame(merge_df[['uid','age_y','gender_x','province_x']].values,columns=bayes_df.columns.values.tolist())
    print temp_df

    temp_df.to_csv('./temp.csv',encoding='utf-8',index=False)
