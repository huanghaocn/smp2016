# coding=utf-8
from elasticsearch import Elasticsearch
from elasticsearch import helpers

host = 'localhost'
port = 9200
index = 'smp'
index_type = 'user'
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
                'status': {
                    'type': 'object',
                    'properties': {
                        'retweet_count': {
                            'type': 'integer'
                        },
                        'review_count': {
                            'type': 'integer'
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
        doc = {
            'uid': cols[0],
            'gender': cols[1],
            'birthday': cols[2],
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
            'fans': fans[1:]
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
        'status': []
    }
    for line in status_file:
        weibo = [t.decode('utf-8') for t in line.strip().split(',')]
        if weibo[0] != doc['uid']:
            if doc['uid'] != 0:
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
                'status': []

            }
        doc['status'].append({
            'retweet_count': int(weibo[1]),
            'review_count': int(weibo[2]),
            'source': weibo[3],
            'time': weibo[4],
            'content': weibo[5]
        })
    # 最后一个人的微博
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
