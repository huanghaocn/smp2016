# coding=utf-8
from utils.maps import resultEncoding
import pandas as pd

__author__ = 'qibai'
origin = "/home/qibai/Documents/smpData/train/cleaned_train_status.txt"
test_status = "/home/qibai/Documents/smpData/test/test_status.txt"
test_nolabel = "../data/test/test_nolabels.txt"
label = "/home/qibai/Documents/smpData/communityDetect/label_maps_without_test.csv"
result = "/home/qibai/result.txt"
output = "/home/qibai/temp.txt"

age_map = {}


def get_train_tgi(up_num=20, up_tgi=0.8):
    age_source_tgi = {'0': {}, '1': {}, '2': {}}
    with open(origin) as trainLines, open(label, 'r') as label_info:
        source_dict = {}
        age_source_dict = {'0': {}, '1': {}, '2': {}}
        label_info_dict = {}
        i = 0
        for line in label_info:
            i += 1
            if i == 1:
                continue
            age = line.split(",")[2]
            label_info_dict[line.split(",")[0]] = age
            if age in age_map:
                age_map[age] += 1
            else:
                age_map[age] = 1
        for line in trainLines:
            items = line.split(",")
            source = items[3]
            if source in source_dict:
                source_dict[source] += 1
            else:
                source_dict[source] = 1
            if source in age_source_dict[label_info_dict[items[0]]]:
                age_source_dict[label_info_dict[items[0]]][source] += 1
            else:
                age_source_dict[label_info_dict[items[0]]][source] = 1

        # for key, val in sorted(source_dict.iteritems(), key=lambda d: d[1], reverse=True):
        #     print key + " " + str(val)
        sum_source_dict_value = sum([num for num in source_dict.values() if num > up_num])
        source_percent_dict = {}
        for key, val in source_dict.items():
            if val <= up_num: continue
            source_percent_dict[key] = float(val) / sum_source_dict_value
        age_source_percent_dict = {}

        for key, val in age_source_dict.items():
            age_source_percent_dict[key] = {}
            sum_age_source_dict_value = sum([num for num in val.values() if num > up_num])
            print key + " age " + str(sum_age_source_dict_value)
            for key2, val2 in val.items():
                if val2 <= up_num: continue
                age_source_percent_dict[key][key2] = float(val2) / sum_age_source_dict_value
                tgi = age_source_percent_dict[key][key2] / source_percent_dict[key2]
                if tgi > up_tgi:
                    age_source_tgi[key][key2] = tgi

        # age_0_set = set(age_source_dict['0'].keys())
        # age_1_set = set(age_source_dict['1'].keys())
        # age_2_set = set(age_source_dict['2'].keys())
        #
        # print "belong 0 age"
        # tmp_0_dict = {}
        # for key in age_0_set-age_1_set-age_2_set:
        #     tmp_0_dict[key] = age_source_dict['0'][key]
        # for key,val in sorted(tmp_0_dict.iteritems(), key=lambda d: d[1], reverse=True):
        #     print key + " " + str(val)
        #
        # print "belong 1 age"
        # tmp_1_dict = {}
        # for key in age_1_set-age_0_set - age_2_set:
        #     tmp_1_dict[key] = age_source_dict['1'][key]
        # for key,val in sorted(tmp_1_dict.iteritems(), key=lambda d: d[1], reverse=True):
        #     print key + " " + str(val)
        #
        # print "belong 2 age"
        # tmp_2_dict = {}
        # for key in age_2_set -age_1_set - age_0_set:
        #     tmp_2_dict[key] = age_source_dict['2'][key]
        # for key,val in sorted(tmp_2_dict.iteritems(), key=lambda d: d[1], reverse=True):
        #     print key + " " + str(val)

        # age_source_dict['0'] = sorted(age_source_dict['0'].iteritems(), key=lambda d: d[1], reverse=True)
        # age_source_dict['1'] = sorted(age_source_dict['1'].iteritems(), key=lambda d: d[1], reverse=True)
        # age_source_dict['2'] = sorted(age_source_dict['2'].iteritems(), key=lambda d: d[1], reverse=True)
        #
        # print "0 age"
        # for key, val in age_source_dict['0']:
        #     print key + " " + str(val)
        # print "1 age"
        # for key, val in age_source_dict['1']:
        #     print key + " " + str(val)
        # print "2 age"
        # for key, val in age_source_dict['2']:
        #     print key + " " + str(val)
        #

        # age_source_percent_dict
        # age_source_percent_dict_0 = sorted(age_source_percent_dict['0'].iteritems(), key=lambda d: d[1], reverse=True)
        # age_source_percent_dict_1 = sorted(age_source_percent_dict['1'].iteritems(), key=lambda d: d[1], reverse=True)
        # age_source_percent_dict_2 = sorted(age_source_percent_dict['2'].iteritems(), key=lambda d: d[1], reverse=True)
        #
        # print "percent_dict 0 age"
        # for key, val in age_source_percent_dict_0:
        #     print key + "," + str(val)
        # print "percent_dict 1 age"
        # for key, val in age_source_percent_dict_1:
        #     print key + "," + str(val)
        # print "percent_dict 2 age"
        # for key, val in age_source_percent_dict_2:
        #     print key + "," + str(val)


        # age_source_tgi
        age_source_tgi_0 = sorted(age_source_tgi['0'].iteritems(), key=lambda d: d[1], reverse=True)
        age_source_tgi_1 = sorted(age_source_tgi['1'].iteritems(), key=lambda d: d[1], reverse=True)
        age_source_tgi_2 = sorted(age_source_tgi['2'].iteritems(), key=lambda d: d[1], reverse=True)

        print "tgi 0 age"
        for key, val in age_source_tgi_0:
            if val > up_tgi:
                print key + "," + str(val)
        print "\n\ntgi 1 age"
        for key, val in age_source_tgi_1:
            if val > up_tgi:
                print key + "," + str(val)
        print "\n\ntgi 2 age"
        for key, val in age_source_tgi_2:
            if val > up_tgi:
                print key + "," + str(val)
    return age_source_tgi


def get_test_source_percent():
    user_source_percent_dict = {}
    source_dict = {}
    with open(test_status) as testLines:
        for line in testLines:
            items = line.split(",")
            uid = items[0]
            if uid not in source_dict:
                source_dict[uid] = {}
            source = items[3]
            if source in source_dict[uid]:
                source_dict[uid][source] += 1
            else:
                source_dict[uid][source] = 1

        # for key, val in sorted(source_dict.iteritems(), key=lambda d: d[1], reverse=True):
        #     print key + " " + str(val)
        for key, val in source_dict.items():
            user_source_percent_dict[key] = {}
            sum_age_source_dict_value = sum(val.values())
            print key + " source num " + str(sum_age_source_dict_value)
            for key2, val2 in val.items():
                user_source_percent_dict[key][key2] = float(val2) / sum_age_source_dict_value

    return user_source_percent_dict


def get_predict(train_tgi, user_percent_dict, alpha=1.0):
    age_predict = {}

    for user_id, sources in user_percent_dict.items():
        age_predict[user_id] = {}
        for age in train_tgi:
            sum_pro = 0
            for key2, val2 in sources.items():
                lapulasi = float(alpha) / len(train_tgi[age])
                if key2 in train_tgi[age]:
                    lapulasi = train_tgi[age][key2]
                sum_pro += val2 * lapulasi
            age_predict[user_id][age] = sum_pro * age_map[age] / sum(age_map.values())

    return age_predict


if __name__ == '__main__':
    train_tgi = get_train_tgi(up_num=17, up_tgi=0.84)
    user_percent_dict = get_test_source_percent()
    predict = get_predict(train_tgi, user_percent_dict, alpha=502)
    result_out = open(result, 'w')
    result_df = pd.read_csv(test_nolabel, index_col=False, header=None, names=['uid'])
    test_uid = result_df.uid.values.tolist()
    for uid in predict:
        if int(uid) not in test_uid: continue
        selected_area_label = max(predict[uid], key=predict[uid].get)
        result_out.write("%s,%s,%s,%s\n" % (uid, selected_area_label, 1, 1))
    result_out.close()
    resultEncoding(result, output)
