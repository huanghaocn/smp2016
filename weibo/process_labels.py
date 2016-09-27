# coding=utf-8
import codecs
from datetime import datetime
import pickle
from utils import maps

with codecs.open('weibo/valid_labels.csv', 'r', 'utf-8') as f_c, open('data/valid/valid_nolabel.txt') as labels, \
        codecs.open('labels_crawled.txt', 'w', 'utf-8') as result:
    # uids = set()
    # for line in f_c:
    #     uids.add(line.split(',')[0])
    # for line in labels:
    #     if line.strip() not in uids:
    #         print line.strip()
    labels = {}
    for line in f_c:
        # gender
        infos = line.strip().split(',')
        uid = infos[0]
        labels[uid] = {}
        if infos[1] == u'男':
            gender = 'm'
        else:
            gender = 'f'
        # birthday
        try:
            year = datetime.strptime(infos[2], '%Y-%m-%d').year
            if year < 1980:
                year = '1979-'
            elif 1980 <= year <= 1989:
                year = '1980-1989'
            else:
                year = '1990+'
        except ValueError:
            print infos[2]
            year = ''
        # location
        location = maps.province2area(infos[3].split(' ')[0])
        labels[uid]['gender'] = gender
        labels[uid]['year'] = year
        labels[uid]['location'] = location
        result.write(uid + ',' + year + ',' + gender + ',' + location + '\n')
    print len(labels)
    with open('labels', 'w') as f:
        pickle.dump(labels, f)
