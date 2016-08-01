import sys
import pickle
import codecs

if __name__ == '__main__':
    if len(sys.argv) == 2:
        with codecs.open(sys.argv[1], encoding='utf-8') as test, open('labels') as labels:
            labels = pickle.load(labels)
            total_count = len(labels)
            correct_gender_count = 0.0
            correct_birthday_count = 0.0
            correct_location_count = 0.0
            for i, line in enumerate(test):
                if i == 0:
                    continue
                infos = line.strip().split(',')
                uid = infos[0]
                if infos[1] == labels[uid]['year']:
                    correct_birthday_count += 1
                if infos[2] == labels[uid]['gender']:
                    correct_gender_count += 1
                if infos[3] == labels[uid]['location']:
                    correct_location_count += 1
            birthday_p = correct_birthday_count / total_count
            gender_p = correct_gender_count / total_count
            location_p = correct_location_count / total_count
            print 'birthday:{:.5f}\ngender:{:^.5f}\nlocation:{:^.5f}\noverall:{:^.5f}'.format(
                    birthday_p, gender_p,
                    location_p, 0.3 * birthday_p + 0.2 * gender_p + 0.5 * location_p)
    else:
        print(
            '''
usage:
    python evaluate.py [filename]
            ''')
