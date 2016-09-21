# -*- coding: utf-8 -*-
__author__ = 'qibai'
import re
labelLines = open("/home/qibai/Documents/smpData/communityDetect/label_maps_without_test.csv")
trainLines = open("/home/qibai/Documents/smpData/train/train_stastu_without_space")
statusLines = open("/home/qibai/Documents/smpData/train/train_status.txt")
#
# items = {}
# area = '3'
# areas = {
#     0: '东北',
#     1: '华北',
#     2: '华东',
#     3: '华中',
#     4: '华南',
#     5: '西南',
#     6: '西北',
#     7: '境外',
#     2333: 'None'
# }
# for line in labelLines:
#     item = line.strip().split(",")
#     # id,gender,age,area
#     if item[3] == area:
#         items[item[0]] = item[3]
# areaText = open("/home/qibai/Documents/smpData/communityDetect/area_" + areas[int(area)] + ".txt", 'w')
# for line in statusLines:
#     if line.split(',')[0] in items:
#         areaText.write(line)
str = u"2528656921,0,0,小米手机2S,2014-01-2912:11:59,快到了但我发誓我憋不住了……[生病]我在:S2611营东高速 显示地图 原图 "
pattern = re.compile('我在')
for line in trainLines:
    match = pattern.match(str)
    if match:
    # 使用Match获得分组信息
        print match.group(1)
