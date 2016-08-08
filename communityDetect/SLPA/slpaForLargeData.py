#!/usr/bin/env python
'''
@author: qibai
'''

import numpy as np
import time
import os


class Slpa:
    """Identify overlapping nodes and overlapping communities in social networks

    Attributes:
       N: number of nodes
       ITERATION: number of iterations
       THRESHHOLD: r => [0,1], if the probability is less than r,
                   remove it during post processing

       adjacency_list: int[N][K] for each node a list of its neighbours' id
       node_memory: [int]{id:count} first dimension is a list of all nodes
                    for each node we have a dictionary keeping the count
                    of the labels it received

    """

    def __init__(self, input_file, mapNum, header_line=True):
        """Initialize the instance with input data

        create adjacency_list after reading the input file

        Args:
            input_file: the file path to the input file
                        The file
        """
        files = [input_file]

        for filename in files:
            if os.path.exists(filename):
                message = 'OK, the "%s" file exists.'
            else:
                message = "Sorry, I cannot find the '%s' file."
            print message % filename



        # f = open("/home/qibai/Documents/smpData/test/test_nolabels.txt", "r")
        # self.test_label_dict = {}
        # for line in f:
        #     uid = line.strip()
        #     uid = int(uid)
        #     self.test_label_dict[uid] = {}
        # f.close()
        # f = open("/home/qibai/Documents/PycharmProjects/smp2016/data-normalized/label_maps.csv", "r")
        #
        # self.train_uid_set = set()
        # for line in f:
        #     if header_line:
        #         header_line = False
        #         continue
        #     user_profile = line.strip().split(',')
        #     uid = user_profile[0]
        #     self.train_uid_set.add(int(uid))
        # f.close()

        self.neghbors_list_bigmap = self.get_neigbors_big_map(input_file, mapNum)
        self.N = self.neghbors_list_bigmap.getLenght()
        print "self.neighbors_bigmap has length %d" % self.N
        # node's memory
        self.labels_memory_bigmap = bigMap(mapNum)
        # init for node's memory
        for uid in self.neghbors_list_bigmap.getKeySet():
            self.labels_memory_bigmap.insert(uid, dict())
            self.labels_memory_bigmap.getMap(uid)[uid] = 1
        # for uid in self.neghbors_list_bigmap.getKeySet():  # for debug
        #     self.neghbors_list_bigmap.insert(uid, set([i for i in self.train_uid_set][0:5]))  # for debug

        print "self.labels_memory has length %d" % self.labels_memory_bigmap.getLenght()

    # init end

    def perform_slpa(self, ITERATION):
        """Performs SLPA algorithm

        Use multinomial sampling for speaker rule
        Use maximum vote for listener rule
        Args:
            TERATION: number of iterations
        """
        self.ITERATION = ITERATION

        userNum = self.labels_memory_bigmap.getLenght()
        for t in range(self.ITERATION):
            start_time = time.time()
            print "Performing %dth iteration..." % t
            processUserNum = 0
            order = np.random.permutation(list(self.labels_memory_bigmap.getKeySet()))  # Nodes.ShuffleOrder()
            for uid in order:  # for each node
                neighbors = self.neghbors_list_bigmap.getMap(uid)
                label_list = {}
                for neighbor in neighbors:  # for each neighbors of the listener
                    # select a label to propagate from speaker neighbor to listener uid
                    if self.labels_memory_bigmap.isExist(neighbor) == False: continue
                    sum_label = sum(self.labels_memory_bigmap.getMap(neighbor).itervalues())
                    if sum_label == 0: continue
                    label_rate = [float(c) / sum_label for c in
                                  self.labels_memory_bigmap.getMap(neighbor).values()]
                    keys = self.labels_memory_bigmap.getMap(neighbor).keys()
                    # use Multinomial Distribution to get label
                    label = keys[np.random.multinomial(1, label_rate).argmax()]
                    if label not in label_list:
                        label_list[label] = 1
                    else:
                        label_list[label] += 1
                if len(label_list) == 0: continue
                # listener chose a received label to add to memory
                selected_label = max(label_list, key=label_list.get)
                # add the selected label to the memory
                if selected_label in self.labels_memory_bigmap.getMap(uid):
                    self.labels_memory_bigmap.getMap(uid)[selected_label] += 1
                else:
                    self.labels_memory_bigmap.getMap(uid)[selected_label] = 1
                processUserNum += 1
                if processUserNum % 100000 == 0:
                    print "Processing " + str((float(processUserNum)) / userNum) + "%"
            end_time = time.time()
            print("this iteration takes %g seconds" % (end_time - start_time))

    # end of perform_slpa

    def post_processing(self, THRESHHOLD):
        """performs post processing to remove the labels that are below the threshhold

        Args:
	    THRESHHOLD: r => [0,1], if the probability is less than r,
                        remove it during post processing
        """
        print "Performing post processing..."

        self.THRESHHOLD = THRESHHOLD

        for uid in self.labels_memory_bigmap.getKeySet():
            memory = self.labels_memory_bigmap.getMap(uid)
            sum_label = sum(memory.itervalues())
            threshhold = sum_label * self.THRESHHOLD
            for k, v in memory.items():
                if v < threshhold:
                    del memory[k]  # remove the outliers
                    # end of the post_processing

    def get_neigbors_big_map(self, neighborsPairs2SideFile, mapNum):
        """
         if form is uid uid , you should transform into {"uid":["uid","uid",...]...}
        :param neighborsPairs2SideFile:
        :return: a dict like above
        """
        input = open(neighborsPairs2SideFile, 'r')
        neighborsListBigMap = bigMap(mapNum)
        i = 0
        for line in input:
            uid1, uid2 = line.strip().split(' ')
            if neighborsListBigMap.isExist(uid1):
                neighborsListBigMap.getMap(uid1).add(int(uid2))
                if len(neighborsListBigMap.getMap(uid1)) > 100000:
                    print 'so big' + uid1 + ' ' + str(len(neighborsListBigMap.getMap(uid1)))
            else:
                neighborsListBigMap.insert(uid1, set())
                neighborsListBigMap.getMap(uid1).add(int(uid2))
                i = i + 1
                if (i % 100000) == 0:
                    print i
                    print  str(neighborsListBigMap.getLenght())
                    neighborsListBigMap.checkBalance()
        #     if neighborsListBigMap.getLenght() == 1000: break  # for debug
        # for u in self.test_label_dict.keys()[0:550]:  # for debug
        #     neighborsListBigMap.insert(u, set())
        input.close()
        return neighborsListBigMap


# end of get_neigbors


class bigMap:
    def __init__(self, mapNum):
        """

        Args:
            mapNum: the number of the map
        """
        self.mapNum = mapNum
        self.lenght = 0
        self.balance = {}
        self.mapsList = list()
        for i in range(mapNum):
            temp = dict()
            self.mapsList.append(temp)

        self.keySet = set()

    # end of __init__
    def checkBalance(self):
        mapNum = self.balance.itervalues()
        temp = sorted(mapNum, reverse=True)
        print 'used map num:' + str(len(temp))
        print 'top dict num:' + str(temp[0:10])

    def insert(self, key, value):
        bucket = int(key) % self.mapNum
        if bucket in self.balance:
            self.balance[bucket] = self.balance[bucket] + 1
        else:
            self.balance[bucket] = 1
        self.mapsList[bucket][int(key)] = value
        self.keySet.add(int(key))

    def getMap(self, key):
        bucket = int(key) % self.mapNum
        return self.mapsList[bucket][int(key)]

    def getLenght(self):
        self.lenght = len(self.keySet)
        return self.lenght

    def isExist(self, key):
        bucket = int(key) % self.mapNum
        return int(key) in self.mapsList[bucket]

    def getKeySet(self):
        return self.keySet


# end of Bigmap class

def main():
    start_time = time.time()
    # windows
    # slpa = Slpa("F:\\allDataProcess\\neighborPairs.txt", "F:\\allDataProcess\\label_maps.csv",
    #             "F:\\allDataProcess\\smpData\\test\\test_nolabels.txt",800)

    # ubuntu
    # slpa = Slpa("/home/qibai/Documents/dataProcess/neighborPairs.txt",
    #             "/home/qibai/Documents/PycharmProjects/smp2016/data-normalized/label_maps.csv",
    #             "/home/qibai/Documents/smpData/test/test_nolabels.txt", 200)

    # server
    slpa = Slpa("/home/zhibin/junxu/smpData/neighborPairs2Side.txt", 20)
    end_time = time.time()
    print("Elapsed time for initialization was %g seconds" % (end_time - start_time))

    start_time = time.time()
    slpa.perform_slpa(50)  # perform slpa for 200 iterations
    end_time = time.time()
    print("Elapsed time for slpa was %g seconds" % (end_time - start_time))

    start_time = time.time()
    slpa.post_processing(0.1)  # perform postprocessing with threshhold 0.1
    end_time = time.time()
    print("Elapsed time for post processing was %g seconds" % (end_time - start_time))

    f = open("/home/zhibin/junxu/smp2016/data-normalized/label_maps.csv", "r")
    trainLabel = open("trainLabelResult.txt", "w+")
    trainLabel.write("trainUid,communityId\n")
    train_label_dict = dict()
    train_community_dict = {}
    for line in f:

        item = line.strip().split(",")
        try:
            uid = int(item[0])
        except:
            continue
        train_label_dict[uid] = ','.join(item[:])
        if slpa.labels_memory_bigmap.isExist(uid):
            train_community_dict[uid] = slpa.labels_memory_bigmap.getMap(uid)
            trainLabel.write(str(uid) + " " + str(train_community_dict[uid])+'\n')
    f.close()
    trainLabel.close()


    f = open("/home/zhibin/junxu/smpData/test/test_nolabels.txt", "r")
    test_label_dict = set()
    testLabel = open("testLabelResult.txt", "w+")
    testLabel.write("testUid,communityId\n")
    find = open("find.txt","w")
    find.write('testUid,testCommunityId,trainLabel,trainCommunityId,togetherCommunityId\n')
    for line in f:
        uid = line.strip()
        uid = int(uid)
        test_label_dict.add(uid)
        if slpa.labels_memory_bigmap.isExist(uid):
            testLabel.write(str(uid) + ' ' + str(slpa.labels_memory_bigmap.getMap(uid))+'\n')
            test_keys = set(slpa.labels_memory_bigmap.getMap(uid).keys())
            for train_id in train_community_dict.keys():
                train_keys = set(train_community_dict[train_id].keys())
                if len(train_keys & test_keys) != 0:
                    find.write(str(uid)+" "+str(slpa.labels_memory_bigmap.getMap(uid))+" "+train_label_dict[train_id]+" "+str(slpa.labels_memory_bigmap.getMap(train_id))+str(train_keys & test_keys)+'\n')
    f.close()
    testLabel.close()
    find.close()
    allLabel = open("allLabelResult.txt", "w+")
    for uid in slpa.labels_memory_bigmap.getKeySet():
        label = slpa.labels_memory_bigmap.getMap(uid)
        allLabel.write("%s %s\n" % (uid, label))
    allLabel.close()  # end of main().


if __name__ == "__main__":
    main()
