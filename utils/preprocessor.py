# coding=utf-8
import re


def weibo_process(content):
    content = re.sub(r'http://t\.cn/\w+\s|\d+|_|￥\s.*\s￥', '', content)
    return content


if __name__ == '__main__':
    print weibo_process('全新 Weico 微博 客户端 iPhone 版 很 棒 ！ 下 一个 试试 看 吧 ！ http://t.cn/zOmTZK7  原 图')
    print weibo_process('￥ AAEDgrPX ￥ [ 星星 ] 淘口令')
