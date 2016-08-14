# -*- coding: utf-8 -*-

"""
@Time    : 16-8-14 下午12:30
@Author  : ino
@Site    : http://ino.design
@File    : uid_content_dict.py
@notes   :
"""
import json

def build_dict():
    with open('../output/test_status_tokenized.json', 'r') as ff:
        dicts = json.load(ff)
        for item in dicts["1746171492"]:
            print item
    ff.close()

if __name__ == '__main__':
    build_dict()
