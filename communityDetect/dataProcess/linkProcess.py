__author__ = 'qibai'
import sys
import time


def getNeighbors(inputFile, neighborPairs, fansNumFile, followNumFile, followAloneList, followEachOtherNumFile):
    lines = open(inputFile, 'r')
    output = open(neighborPairs, 'w')  # uid1 uid2 means uid1 and uid2 follow each other
    fansNumFileOutput = open(fansNumFile, 'w')  # uid has fans number
    followNumFileOutput = open(followNumFile, 'w')  # uid follow other user number
    followAloneListOutput = open(followAloneList, 'w')  # uid follow alonely other user'uid
    followEachOtherNumFileOutput = open(followEachOtherNumFile, 'w')  # uid follow each other number
    neighborDict = {}
    statNumDict = {}
    statEachOtherNum = {}
    for line in lines:
        line = line.strip('\n')
        ids = line.split(' ')
        id = ids[0]
        neighborSet = set(ids[1:])
        if id in neighborDict:
            print 'duplicate key:' + id
            continue
        fansNumFileOutput.write(id + " " + str(len(neighborSet)) + '\n')
        friends = set()
        for fansid in neighborSet:
            if fansid in statNumDict:
                statNumDict[fansid] = statNumDict[fansid] + 1
            else:
                statNumDict[fansid] = 1
            if (fansid in neighborDict) and (fansid != id):
                fansNeighborSet = neighborDict[fansid]
                if id in fansNeighborSet:
                    fansNeighborSet.remove(id)
                    output.write(id + ' ' + fansid + '\n')
                    if id in statEachOtherNum:
                        statEachOtherNum[id] = statEachOtherNum[id] + 1
                    else:
                        statEachOtherNum[id] = 1
                    if fansid in statEachOtherNum:
                        statEachOtherNum[fansid] = statEachOtherNum[fansid] + 1
                    else:
                        statEachOtherNum[fansid] = 1

                friends.add(fansid)
        neighborSet = neighborSet - friends
        neighborDict[id] = neighborSet

    for userId in statNumDict:
        followNumFileOutput.write(userId + ' ' + str(statNumDict[userId]) + '\n')
    for userId in statEachOtherNum:
        followEachOtherNumFileOutput.write(userId + ' ' + str(statEachOtherNum[userId]) + '\n')
    for userId in neighborDict:
        followAloneListOutput.write(userId + ' ' + ' '.join(neighborDict.get(userId)) + '\n')
    lines.close()
    output.close()
    fansNumFileOutput.close()
    followNumFileOutput.close()
    followEachOtherNumFileOutput.close()
    followAloneListOutput.close()
    print "get neighbors done"


def getNeigborsList(neighborsFile, neighborsList):
    input = open(neighborsFile, 'r')
    neighborsListOutput = open(neighborsList, 'w')
    neighborsListDict = {}
    for line in input:
        uid1, uid2 = line.strip().split(' ')
        if uid1 in neighborsListDict:
            neighborsListDict[uid1].add(uid2)
        else:
            neighborsListDict[uid1] = set()
            neighborsListDict[uid1].add(uid2)
        if uid2 in neighborsListDict:
            neighborsListDict[uid2].add(uid1)
        else:
            neighborsListDict[uid2] = set()
            neighborsListDict[uid2].add(uid1)

    for key in neighborsListDict:
        neighbors = ' '.join(neighborsListDict[key])
        neighborsListOutput.write(key + ' ' + neighbors + '\n')
    neighborsListOutput.close()
    input.close()
    print "get neighbors list done"


def getNeigborsListFromPairs2Side(neighborsPairs2SideFile, neighborsList):
    input = open(neighborsPairs2SideFile, 'r')
    neighborsListOutput = open(neighborsList, 'w')
    neighborsListDict = {}
    for line in input:
        uid1, uid2 = line.strip().split(' ')
        if uid1 in neighborsListDict:
            neighborsListDict[uid1].add(uid2)
        else:
            neighborsListDict[uid1] = set()
            neighborsListDict[uid1].add(uid2)
    for key in neighborsListDict:
        neighbors = ' '.join(neighborsListDict[key])
        neighborsListOutput.write(key + ' ' + neighbors + '\n')
    neighborsListOutput.close()
    input.close()
    print "get neighbors list from 2 side pairs done"


def getNeigborsPairs(neighborsFile, neighborPairs2Side):
    input = open(neighborsFile, 'r')
    neighborsPairsOutput = open(neighborPairs2Side, 'w')
    for line in input:
        uid1, uid2 = line.strip().split(' ')
        neighborsPairsOutput.write(uid1 + ' ' + uid2 + '\n')
        neighborsPairsOutput.write(uid2 + ' ' + uid1 + '\n')
    neighborsPairsOutput.close()
    input.close()
    print "get neighbors pairs done"


def merge(files, outputFile):
    output = open(outputFile, 'w')
    # files = []
    # files.append(file1)
    # files.append(file2)
    # files.append(file3)
    for file in files:
        input = open(file, 'r')
        for line in input:
            output.write(line)
        input.close()
    output.close()
    print "merge file done"


def appendTrainAndTestLink(trainLabel, trainLinks, testLabel, testLinks, neighborPairs, unlabelLink,
                           neighborPairs2Side):
    output = open(neighborPairs2Side, 'a')
    uids = set()
    trainAppended = set()
    testAppended = set()
    trainUidSet = set()
    testUidSet = set()
    input = open(neighborPairs, 'r')
    for line in input:
        line = line.strip()
        uid1, uid2 = line.split(' ')
        uids.add(uid1)
        uids.add(uid2)
    input.close()
    input = open(trainLabel, 'r')
    for line in input:
        id = line.strip().split("||")[0]
        if id not in uids:
            trainUidSet.add(id)
    input.close()
    print "train doesn't cover size " + str(len(trainUidSet))
    input = open(testLabel, 'r')
    for line in input:
        id = line.strip()
        if id not in uids:
            testUidSet.add(id)
    input.close()
    print "test doesn't cover size " + str(len(testUidSet))
    input = open(unlabelLink, 'r')
    for line in input:
        ids = line.strip().split(' ')
        uid = ids[0]
        for id in ids[1:]:
            if id in trainUidSet:
                if uid in uids:
                    output.write(uid + ' ' + id + '\n')
                    trainAppended.add(id)
                else:
                    print 'traing set outliers:unlabel uid : ' + uid + ' trainId ' + id
            if id in testUidSet:
                if uid in uids:
                    output.write(id + ' ' + uid + '\n')
                    testAppended.add(id)
                else:
                    print 'test set outliers:unlabel uid : ' + uid + ' testId ' + id
    input.close()
    print "train didn't append uid size :" + str(len(trainUidSet - trainAppended)) + str(trainUidSet - trainAppended)
    print "test didn't append uid size :" + str(len(testUidSet - testAppended)) + str(testUidSet - testAppended)
    input = open(trainLinks, 'r')
    for line in input:
        ids = line.strip().split(' ')
        uid = ids[0]
        for id in ids[1:]:
            if uid in trainUidSet:
                if id in uids:
                    output.write(id + ' ' + uid + '\n')
                    trainAppended.add(uid)
                else:
                    print 'traing set outliers:unlabel uid : ' + uid + ' trainId ' + id
    input.close()
    input = open(testLinks, 'r')
    for line in input:
        ids = line.strip().split(' ')
        uid = ids[0]
        for id in ids[1:]:
            if uid in testUidSet:
                if id in uids:
                    output.write(uid + ' ' + id + '\n')
                    testAppended.add(uid)
                else:
                    print 'test set outliers:unlabel uid : ' + uid + ' testId ' + id
    input.close()
    print "train didn't append uid size :" + str(len(trainUidSet - trainAppended)) + str(trainUidSet - trainAppended)
    print "test didn't append uid size :" + str(len(testUidSet - testAppended)) + str(testUidSet - testAppended)
    output.close()
    print "append train and test link done"


def findDuplicate(trainLabel, testLabel, unlabelLink):
    trainUidSet = set()
    testUidSet = set()
    input = open(trainLabel, 'r')
    for line in input:
        id = line.strip().split("||")[0]
        trainUidSet.add(id)
    input.close()
    input = open(testLabel, 'r')
    for line in input:
        id = line.strip()
        testUidSet.add(id)
    input.close()
    input = open(unlabelLink, 'r')
    for line in input:
        ids = line.strip().split(' ')
        id = ids[0]
        if (id in trainUidSet) or (id in testUidSet):
            print "DuplicateKey:" + id
    print "find duplicateKey done"


if __name__ == "__main__":
    start_time = time.time()

    home = "smpData/"
    findDuplicate(home + "train/train_labels.txt", home + "test/test_nolabels.txt",
                  home + "unlabeled_links/other_links.txt")
    merge([home + "train/train_links.txt", home + "test/test_links.txt",
           home + "unlabeled_links/other_links.txt"], home + "allLinks.txt")
    getNeighbors(home + "allLinks.txt", home + "neighborPairs.txt", home + "fansNum.txt",
                 home + "followNum.txt", home + "followAloneList.txt",
                 home + "followEachOtherNum.txt")
    # getNeigborsList(home + "neighborPairs.txt", home+"neighborList.txt")
    getNeigborsPairs(home + "neighborPairs.txt", home + "neighborPairs2Side.txt")
    appendTrainAndTestLink(home + "train/train_labels.txt", home + "train/train_links.txt",
                           home + "test/test_nolabels.txt",
                           home + "test/test_links.txt", home + "neighborPairs.txt",
                           home + "unlabeled_links/other_links.txt",
                           home + "neighborPairs2Side.txt")
    end_time = time.time()
    print("Elapsed time for data processing was %g seconds" % (end_time - start_time))
