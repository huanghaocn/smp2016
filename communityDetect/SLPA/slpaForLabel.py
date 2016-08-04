#!/usr/bin/env python
'''
@author: qibai
'''

import numpy as np
import time
import operator


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

    def __init__(self, input_file, train_label_file, test_label_file, mapNum, header_line=True):
        """Initialize the instance with input data

        create adjacency_list after reading the input file

        Args:
            input_file: the file path to the input file
                        The file
        """
        f = open(test_label_file, "r")
        self.test_label_dict = {}
        for line in f:
            uid = line.strip()
            self.test_label_dict[uid] = {}
            self.test_label_dict[uid]['gender'] = 0
            self.test_label_dict[uid]['age'] = 0
            self.test_label_dict[uid]['area'] = 0
        f.close()

        self.neghbors_list_bigmap = self.get_neigbors_big_map(input_file, mapNum)
        self.N = self.neghbors_list_bigmap.getLenght()
        print "self.train_label has length %d" % self.N
        print "self.test_label has length %d" % len(self.test_label_dict)
        # node's memory
        self.labels_memory_bigmap = bigMap(mapNum)
        # init for train data
        f = open(train_label_file, "r")
        self.train_uid_set = set()
        for line in f:
            if header_line:
                header_line = False
                continue
            user_profile = line.strip().split(',')
            uid = user_profile[0]
            self.train_uid_set.add(uid)
            gender = user_profile[1]
            age = user_profile[2]
            area = user_profile[3]
            self.labels_memory_bigmap.insert(uid, dict())
            self.labels_memory_bigmap.getMap(uid)['gender'] = {}
            self.labels_memory_bigmap.getMap(uid)['age'] = {}
            self.labels_memory_bigmap.getMap(uid)['area'] = {}
            self.labels_memory_bigmap.getMap(uid)['gender'][gender] = 1
            self.labels_memory_bigmap.getMap(uid)['age'][age] = 1
            self.labels_memory_bigmap.getMap(uid)['area'][area] = 1
        f.close()

        # init for node's memory
        for uid in self.neghbors_list_bigmap.getKeySet():
            if uid in self.train_uid_set:
                continue
            self.labels_memory_bigmap.insert(uid, dict())
            self.labels_memory_bigmap.getMap(uid)['gender'] = {}
            self.labels_memory_bigmap.getMap(uid)['age'] = {}
            self.labels_memory_bigmap.getMap(uid)['area'] = {}
        #for uid in self.neghbors_list_bigmap.getKeySet(): #for debug
            #self.neghbors_list_bigmap.insert(uid,set([i for i in self.train_uid_set][0:5]))   # for debug

        print "self.labels_memory has length %d" % self.labels_memory_bigmap.getLenght()

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
                neighborsListBigMap.getMap(uid1).add(uid2)
                if len(neighborsListBigMap.getMap(uid1))>100000:
                    print 'so big'+uid1+' '+ str(len(neighborsListBigMap.getMap(uid1)))
            else:
                neighborsListBigMap.insert(uid1, set())
                neighborsListBigMap.getMap(uid1).add(uid2)
                i = i + 1
                if (i % 100000) ==0:
                    print i
                    print  str(neighborsListBigMap.getLenght())
                    neighborsListBigMap.checkBalance()
            #if neighborsListBigMap.getLenght() == 1000: break  # for debug
        #for u in self.test_label_dict:  # for debug
            #neighborsListBigMap.insert(u,set())
        input.close()
        return neighborsListBigMap

    # end of get_neigbors

    def perform_slpa(self, ITERATION, change=0.001):
        """Performs SLPA algorithm

        Use multinomial sampling for speaker rule
        Use maximum vote for listener rule
        Args:
            TERATION: number of iterations
        """
        self.ITERATION = ITERATION

        last_rate_total = 0
        for t in range(self.ITERATION):
            print "Performing %dth iteration..." % t
            # order = np.random.permutation(self.labels_memory_dict.keys())  # Nodes.ShuffleOrder()
            for uid in self.labels_memory_bigmap.getKeySet():  # for each node
                if uid in self.train_uid_set: continue
                neighbors = self.neghbors_list_bigmap.getMap(uid)
                for label_type in self.labels_memory_bigmap.getMap(uid):
                    label_list = {}
                    for neighbor in neighbors:  # for each neighbors of the listener
                        # select a label to propagate from speaker neighbor to listener uid
                        if self.labels_memory_bigmap.isExist(neighbor) == False: continue
                        sum_label = sum(self.labels_memory_bigmap.getMap(neighbor)[label_type].itervalues())
                        if sum_label == 0: continue
                        label_rate = [float(c) / sum_label for c in
                                      self.labels_memory_bigmap.getMap(neighbor)[label_type].values()]
                        keys = self.labels_memory_bigmap.getMap(neighbor)[label_type].keys()
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
                    if uid in self.test_label_dict:
                        self.test_label_dict[uid][label_type] = 1
                    if selected_label in self.labels_memory_bigmap.getMap(uid)[label_type]:
                        self.labels_memory_bigmap.getMap(uid)[label_type][selected_label] += 1
                    else:
                        self.labels_memory_bigmap.getMap(uid)[label_type][selected_label] = 1
            sum_gender = sum_age = sum_area = 0
            for uid in self.test_label_dict:
                if self.test_label_dict[uid]['gender'] != 0:
                    sum_gender += 1
                if self.test_label_dict[uid]['age'] != 0:
                    sum_age += 1
                if self.test_label_dict[uid]['area'] != 0:
                    sum_area += 1
            test_len = len(self.test_label_dict)
            rate = [float(sum_gender) / test_len, float(sum_age) / test_len, float(sum_area) / test_len]
            print "test set cover gender %f age %f area %f " % (rate[0], rate[1], rate[2])
            rate_total = float(sum(rate)) / 3
            if (rate_total - last_rate_total < change) and (rate_total > 0.85):
                break
            last_rate_total = rate_total

    # end of perform_slpa

    def post_processing(self, THRESHHOLD):
        """performs post processing to remove the labels that are below the threshhold

        Args:
	    THRESHHOLD: r => [0,1], if the probability is less than r,
                        remove it during post processing
        """
        print "Performing post processing..."

        self.THRESHHOLD = THRESHHOLD

        for uid in self.test_label_dict:
            if self.labels_memory_bigmap.isExist(uid)==False:
                print "can't predict " + uid
                continue
            for label_type in self.labels_memory_bigmap.getMap(uid):
                memory = self.labels_memory_bigmap.getMap(uid)[label_type]
                sum_label = sum(memory.itervalues())
                threshhold = sum_label * self.THRESHHOLD
                for k, v in memory.items():
                    if v < threshhold:
                        del memory[k]  # remove the outliers
                self.test_label_dict[uid][label_type] = {}
                sum_label = sum(memory.itervalues())
                for k, v in memory.items():
                    self.test_label_dict[uid][label_type][k] = float(v) / sum_label

                    # end of post_processing  # end of Slpa class


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
        temp = sorted(mapNum,reverse=True)
        print 'used map num:'+str(len(temp))
        print 'top dict num:'+str(temp[0:10])
    def insert(self, key, value):
        bucket = int(key) % self.mapNum
        if bucket in self.balance:
            self.balance[bucket] = self.balance[bucket]+1
        else:
            self.balance[bucket] = 1
        self.mapsList[bucket][key] = value
        self.keySet.add(key)

    def getMap(self, key):
        bucket = int(key) % self.mapNum
        return self.mapsList[bucket][key]

    def getLenght(self):
        self.lenght = len(self.keySet)
        return self.lenght

    def isExist(self, key):
        bucket = int(key) % self.mapNum
        return key in self.mapsList[bucket]

    def getKeySet(self):
        return self.keySet


# end of Bigmap class

def main():
    start_time = time.time()
    slpa = Slpa("F:\\allDataProcess\\neighborPairs.txt", "F:\\allDataProcess\\label_maps.csv",
                "F:\\allDataProcess\\smpData\\test\\test_nolabels.txt",800)
    # slpa = Slpa("../dataProcess/smpData/neighborPairs2Side.txt", "../dataProcess/smpData/label_maps.csv",
    #             "../dataProcess/smpData/test/test_nolabels.txt",800)
    end_time = time.time()
    print("Elapsed time for initialization was %g seconds" % (end_time - start_time))

    start_time = time.time()
    slpa.perform_slpa(200)  # perform slpa for 200 iterations
    end_time = time.time()
    print("Elapsed time for slpa was %g seconds" % (end_time - start_time))

    start_time = time.time()
    slpa.post_processing(0.1)  # perform postprocessing with threshhold 0.1
    end_time = time.time()
    print("Elapsed time for post processing was %g seconds" % (end_time - start_time))

    rate_out = open("rateTemp.csv", "w+")
    result_out = open("temp.csv", "w+")
    rate_out.write("uid,age,gender,province\n")
    result_out.write("uid,age,gender,province\n")
    for uid in slpa.test_label_dict:
        label = slpa.test_label_dict[uid]
        selected_age_label = max(slpa.test_label_dict[uid]['age'], key=slpa.test_label_dict[uid]['age'].get)
        selected_gender_label = max(slpa.test_label_dict[uid]['gender'], key=slpa.test_label_dict[uid]['gender'].get)
        selected_area_label = max(slpa.test_label_dict[uid]['area'], key=slpa.test_label_dict[uid]['area'].get)
        rate_out.write("%s %s %s %s\n" % (uid, label['age'], label['gender'], label['area']))
        result_out.write("%s,%s,%s,%s\n" % (uid, selected_age_label, selected_gender_label, selected_area_label))
    result_out.close()


# end of main().

if __name__ == "__main__":
    # test = {}
    # for i in range(4000000):
    #     test[str(i*1000)]=set()
    #     if i%100000==0:print i

    main()
