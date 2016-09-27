# coding=utf-8
import re


def weibo_process(content, no_space):
    content = re.sub(r'http://t\.cn/\w+|\d+|_|￥\s.*\s￥', '', content)
    if no_space:
        content = re.sub(r'\s', '', content)
    return content


if __name__ == '__main__':
    print weibo_process('全新 Weico 微博 客户端 iPhone 版 很 棒 ！ 下 一个 试试 看 吧 ！ http://t.cn/zOmTZK7  原 图', False)
    print weibo_process('￥ AAEDgrPX ￥ [ 星星 ] 淘口令', True)
    print weibo_process('！）】　http://t.cn/aKKmt　投给""天蝎座""这个', True)
