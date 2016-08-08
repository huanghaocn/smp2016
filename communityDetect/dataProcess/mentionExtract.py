# -*- coding: utf-8 -*-

__author__ = 'qibai'
import re


def formatText(textFile, formatFile):
    input = open(textFile, 'r')
    output = open(formatFile, 'w')

    for line in input:
        a = " 你 知道 吗".replace(" ", '')
        print a


if __name__ == '__main__':
    email = "754821000@qq.com"
    print email.find('@qq')
    p1 = re.compile('(.+?)@qq')
    emailmatch = p1.match(email)
    if emailmatch:
        print emailmatch.group(1)
    else:
        print 'email address is error!'
