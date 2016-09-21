__author__ = 'qibai'

# -*- coding:utf-8 -*-
import urllib
path = "/home/qibai/Documents/smpData/valid_images/"

lines = open("/home/qibai/Documents/smpData/valid/valid_info.txt")
for line in lines:
    item = line.strip().split("||")
    url = item[2]
    name = item[0]
    try:
        conn = urllib.urlopen(url)
    except:
        print "None"
        continue
    f = open(path+name,'wb')
    f.write(conn.read())
    f.close()
print('Pic Saved!')