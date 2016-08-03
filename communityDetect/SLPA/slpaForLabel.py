#!/usr/bin/env python
'''
Created on Oct 12, 2013

@author: yiping
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

    def __init__(self, input_file, train_label_file, test_label_file, header_line=True):
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
        self.neighbors_list_dict = self.get_neigbors(input_file)
        self.N = len(self.neighbors_list_dict)
        print "self.train_label has length %d" % self.N
        print "self.test_label has length %d" % len(self.test_label_dict)
        # node's memory
        self.labels_memory_dict = {}

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
            self.labels_memory_dict[uid] = {}
            self.labels_memory_dict[uid]['gender'] = {}
            self.labels_memory_dict[uid]['age'] = {}
            self.labels_memory_dict[uid]['area'] = {}
            self.labels_memory_dict[uid]['gender'][gender] = 1
            self.labels_memory_dict[uid]['age'][age] = 1
            self.labels_memory_dict[uid]['area'][area] = 1
        f.close()

        # init for node's memory
        for uid in self.neighbors_list_dict:
            if uid in self.train_uid_set:
                continue
            self.labels_memory_dict[uid] = {}
            self.labels_memory_dict[uid]['gender'] = {}
            self.labels_memory_dict[uid]['age'] = {}
            self.labels_memory_dict[uid]['area'] = {}
            self.neighbors_list_dict[uid] = set([i for i in self.train_uid_set][0:5])  # for debug

        print "self.labels_memory has length %d" % len(self.labels_memory_dict)

    # end of __init__


    def get_neigbors(self, neighborsPairs2SideFile):
        """
         if form is uid uid , you should transform into {"uid":["uid","uid",...]...}
        :param neighborsPairs2SideFile:
        :return: a dict like above
        """
        input = open(neighborsPairs2SideFile, 'r')
        neighborsListDict = {}
        for line in input:
            uid1, uid2 = line.strip().split(' ')
            if uid1 in neighborsListDict:
                neighborsListDict[uid1].add(uid2)
            else:
                neighborsListDict[uid1] = set()
                neighborsListDict[uid1].add(uid2)
            if len(neighborsListDict) == 1000: break  # for debug
        for u in self.test_label_dict:  # for debug
            neighborsListDict[u] = set()
        input.close()
        return neighborsListDict

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
            order = np.random.permutation(self.labels_memory_dict.keys())  # Nodes.ShuffleOrder()
            for uid in order:  # for each node
                if uid in self.train_uid_set: continue
                neighbors = self.neighbors_list_dict[uid]
                for label_type in self.labels_memory_dict[uid]:
                    label_list = {}
                    for neighbor in neighbors:  # for each neighbors of the listener
                        # select a label to propagate from speaker neighbor to listener uid
                        if neighbor not in self.labels_memory_dict: continue
                        sum_label = sum(self.labels_memory_dict[neighbor][label_type].itervalues())
                        if sum_label == 0: continue
                        label_rate = [float(c) / sum_label for c in
                                      self.labels_memory_dict[neighbor][label_type].values()]
                        keys = self.labels_memory_dict[neighbor][label_type].keys()
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
                    if selected_label in self.labels_memory_dict[uid][label_type]:
                        self.labels_memory_dict[uid][label_type][selected_label] += 1
                    else:
                        self.labels_memory_dict[uid][label_type][selected_label] = 1
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
            if uid not in self.labels_memory_dict:
                print "can't predict " + uid
                continue
            for label_type in self.labels_memory_dict[uid]:
                memory = self.labels_memory_dict[uid][label_type]
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


def main():
    start_time = time.time()
    slpa = Slpa("F:\\allDataProcess\\neighborPairs.txt", "F:\\allDataProcess\\label_maps.csv",
                "F:\\allDataProcess\\smp cup data\\test\\test_nolabels.txt")
    end_time = time.time()
    print("Elapsed time for initialization was %g seconds" % (end_time - start_time))

    start_time = time.time()
    slpa.perform_slpa(20)  # perform slpa for 20 iterations
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
    main()
