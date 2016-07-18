from glob import glob
from collections import defaultdict
from pprint import pprint

dataset_root = '../season_2/*/'


def getFileDict(dataFolder):
    dataFiles = defaultdict(list)
    for item in dataFolder:
        for f_name in glob(item + '/*'):
            dataFiles[f_name.split('/')[-1].split('_')[0]].append(f_name)
    for v in dataFiles.itervalues():
        v.sort()
    return dataFiles


def getTrainFiles():
    trainTestData = glob(dataset_root)
    trainFolder = trainTestData[-1]
    trainDataFolders = glob(trainFolder + '/*/')
    dataFiles = getFileDict(trainDataFolders)
    trainDataFiles = {'train_' + k: v for k, v in dataFiles.iteritems()}
    return dict(trainDataFiles)


def getTestFiles():
    trainTestData = glob(dataset_root)
    testFolder = trainTestData[0]
    testDataFolders = glob(testFolder + '/*/')
    dataFiles = getFileDict(testDataFolders)
    dataFiles['prediction'] = glob(testFolder + '/*.txt')
    testDataFiles = {'test_' + k: v for k, v in dataFiles.iteritems()}
    return dict(testDataFiles)


def getFiles(folder, name):
    Files = {}
    nameKey = [key for key in folder.keys() if name in key][0]
    for idx, val in enumerate(folder[nameKey]):
        if idx < 9:
            dat = '_data_0'
        else:
            dat = '_data_'
        Files[nameKey + dat + str(idx + 1)] = val
    return Files


def getAllFiles(train=None, test=None, *args):
    if not args:
        args = ['cluster', 'order', 'weather', 'traffic', 'poi']
    testFileNames = {}
    trainFileNames = {}
    if train:
        trainFiles = getTrainFiles()
        for fname in args:
            trainFileNames[fname] = (getFiles(trainFiles, fname))
    if test:
        testFiles = getTestFiles()
        for fname in args:
            testFileNames[fname] = (getFiles(testFiles, fname))
        testFileNames['prediction'] = (getFiles(testFiles, 'prediction'))
    return trainFileNames, testFileNames


if __name__ == '__main__':
    trainfiles, testfiles = getAllFiles(test=True, train=False)
    pprint(trainfiles)
    pprint(testfiles)
