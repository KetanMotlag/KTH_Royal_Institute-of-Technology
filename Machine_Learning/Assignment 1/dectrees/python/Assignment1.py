import dtree as d
import monkdata as m
import math
import random

#v1 = dtree.entropy(monkdata.monk1)
#print(v1)
#v2 = dtree.entropy(monkdata.monk2)
#print(v2)
#v3 = dtree.entropy(monkdata.monk3)
#print(v3)

print("###########################################################################")


class DecisionTree:
    def __init__(self, dataset, name):
        self.dataset = dataset
        self.name = name


trainingset = [DecisionTree(m.monk1, "monk1TrainingData"),
               DecisionTree(m.monk2, "monk2TrainingData"),
               DecisionTree(m.monk3, "monk3TrainingData")]

testset = [DecisionTree(m.monk1test, "monk1TestData"),
           DecisionTree(m.monk2test, "monk2TestData"),
           DecisionTree(m.monk3test, "monk3TestData")]


def calculateEntropyOfTrainingData():
    for set in trainingset:
        print("Entropy of " + set.name + " : " + str(d.entropy(set.dataset)))
    print("")


calculateEntropyOfTrainingData()


def calculateInformationGain():
    for set in trainingset:
        getAverageInformationGain(set.dataset, set.name)


def getAverageInformationGain(dataset, name):
    print("Information Gain of:" + name + ":")
    for i in range(len(m.attributes)):
        print("InformationGain of " + name + " " + m.attributes[i].name + " : " + str(
            d.averageGain(dataset, m.attributes[i])))
    print("The Best Attribute for splitting the result " + name + ":" + str(d.bestAttribute(dataset, m.attributes)))


calculateInformationGain()


def splittingHighestAttribute():
    a5 = m.attributes[4]
    for set in trainingset:
        for attibuteValues in a5.values:
            subset = d.select(set.dataset, a5, attibuteValues)
            getAverageInformationGain(subset, set.name + "on A5 = " + str(attibuteValues))


splittingHighestAttribute()


def buildTreeFromMonk1Data():
    for i in range(len(trainingset) - 2):
        tree = d.buildTree(trainingset[i].dataset, m.attributes, maxdepth=3)
        qt.drawTree(tree)

buildTreeFromMonk1Data()
