# coding=utf-8
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import time

host = 'localhost'
port = 9200
index = 'smp'
index_type = 'user'

north_east = [u'辽宁', u'吉林', u'黑龙江'],
north = [u'河北', u'山西', u'内蒙古', u'北京', u'天津']
east = [u'山东', u'江苏', u'安徽', u'浙江', u'台湾', u'福建', u'江西', u'上海']
center = [u'河南', u'湖北', u'湖南']
south = [u'广东', u'广西', u'海南', u'香港', u'澳门']
south_west = [u'云南', u'贵州', u'四川', u'西藏']
north_west = [u'新疆', u'陕西', u'宁夏', u'青海', u'甘肃']

mapping = {
    'mappings': {
        index_type: {
            'properties': {
                'uid': {
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'screen_name': {
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'avatar_large': {
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'gender': {
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'birthday': {
                    'type': 'date',
                },
                'location': {
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'location0': {
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'location1': {
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'fans': {
                    'type': 'string',
                    'index': 'not_analyzed'
                },
                'fans_count': {
                    'type': 'long'
                },
                'status_count': {
                    'type': 'long'
                },
                'retweet_count': {
                    'type': 'long'
                },
                'review_count': {
                    'type': 'long'
                },
                'status': {
                    'type': 'object',
                    'properties': {
                        'retweet_count': {
                            'type': 'long'
                        },
                        'review_count': {
                            'type': 'long'
                        },
                        'source': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        },
                        'time': {
                            'type': 'date',
                            'format': 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd HH:mm||epoch_millis',
                            'ignore_malformed': 'true'
                        },
                        'hour': {
                            'type': 'integer'
                        },
                        'content': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                }
            }
        }
    }
}

# 库已经存在就删除重建
es = Elasticsearch(host=host, port=port)
if es.indices.exists(index):
    es.indices.delete(index)
es.indices.create(index, body=mapping)


def info_actions(info_file):
    for line in info_file:
        cols = [col.decode('utf-8') if col != 'None' else None for col in line.strip().split('||')]
        doc = {
            'uid': cols[0],
            'screen_name': cols[1],
            'avatar_large': cols[2]
        }
        action = {
            '_op_type': 'update',
            '_index': index,
            '_type': index_type,
            '_id': cols[0],
            'upsert': doc,
            'doc': doc
        }
        yield action


def labels_actions(labels_file):
    for line in labels_file:
        cols = [col.decode('utf-8') if col != 'None' else None for col in line.strip().split('||')]
        locations = [l if l != 'None' else None for l in cols[3].split(' ')]
        if locations[0] in north_east:
            location = u'东北'
        elif locations[0] in north:
            location = u'华北'
        elif locations[0] in east:
            location = u'华东'
        elif locations[0] in center:
            location = u'华中'
        elif locations[0] in south:
            location = u'华南'
        elif locations[0] in south_west:
            location = u'西南'
        elif locations[0] in south:
            location = u'华南'
        else:
            location = u'境外'
        doc = {
            'uid': cols[0],
            'gender': cols[1],
            'birthday': cols[2],
            'location': location,
            'location0': locations[0],
            'location1': locations[1]
        }
        action = {
            '_op_type': 'update',
            '_index': index,
            '_type': index_type,
            '_id': cols[0],
            'upsert': doc,
            'doc': doc
        }
        yield action


def links_actions(links_file):
    for line in links_file:
        fans = line.strip().split(' ')
        doc = {
            'uid': fans[0],
            'fans': fans[1:],
            'fans_count': len(fans) - 1
        }
        action = {
            '_op_type': 'update',
            '_index': index,
            '_type': index_type,
            '_id': fans[0],
            'upsert': doc,
            'doc': doc
        }
        yield action


def status_actions(status_file):
    doc = {
        'uid': '0',
        'retweet_count': 0,
        'review_count': 0,
        'status': []
    }
    for line in status_file:
        weibo = [t.decode('utf-8') for t in line.strip().split(',')]
        if weibo[0] != doc['uid']:
            if doc['uid'] != 0:
                doc['status_count'] = len(doc['status'])
                yield {
                    '_op_type': 'update',
                    '_index': index,
                    '_type': index_type,
                    '_id': doc['uid'],
                    'upsert': doc,
                    'doc': doc
                }
            doc = {
                'uid': weibo[0],
                'status': [],
                'retweet_count': 0,
                'review_count': 0,
            }
        try:
            hour = time.strptime(weibo[4], '%Y-%m-%d %H:%M:%S').tm_hour
        except ValueError:
            try:
                hour = time.strptime(weibo[4] + ':00', '%Y-%m-%d %H:%M:%S').tm_hour
            except ValueError:
                hour = -1
                print weibo[4]
        doc['status'].append({
            'retweet_count': int(weibo[1]),
            'review_count': int(weibo[2]),
            'source': weibo[3],
            'time': weibo[4],
            'hour': hour,
            'content': weibo[5]
        })
        doc['retweet_count'] += int(weibo[1])
        doc['review_count'] += int(weibo[2])
    # 最后一个人的微博
    doc['status_count'] = len(doc['status'])
    yield {
        '_op_type': 'update',
        '_index': index,
        '_type': index_type,
        '_id': doc['uid'],
        'upsert': doc,
        'doc': doc
    }


if __name__ == '__main__':
    with open('data/train/train_info.txt') as info, open('data/train/train_labels.txt') as labels, \
            open('data/train/train_links.txt') as links, open('data/train/train_status.txt') as status, \
            open('data/other_links.txt') as other_links, open('data/unlabeled_statuses.txt') as ul_status:
        helpers.bulk(es, info_actions(info))
        helpers.bulk(es, labels_actions(labels))
        helpers.bulk(es, links_actions(links))
        helpers.bulk(es, status_actions(status))
        # helpers.bulk(es, links_actions(other_links))
        # helpers.bulk(es, status_actions(ul_status))
