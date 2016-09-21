__author__ = 'qibai'

with open("../data/train/train_labels.txt", 'r')as train_record, open("../data/test/test_nolabels.txt") as test_record, \
        open("/home/qibai/Documents/smpData/neighborPairs2Side.txt")as neighbors:
    train_ids = set()
    for line in train_record:
        train_ids.add(line.split("||")[0])
    test_ids = set()
    for line in test_record:
        test_ids.add(line.strip())

    i = 0
    for line in neighbors:
        user1, user2 = line.strip().split(" ")
        if ((user1 in train_ids) and (user2 in test_ids)) or ((user2 in train_ids) and (user1 in test_ids)):
            i += 1
            print user1+" "+user2+" "+str(i)
