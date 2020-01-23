import random
import dtree as d 
import monkdata as m
import drawtree_qt4 as qt

class DecisionTree:
    def __init__(self,dataset,name):
        self.dataset= dataset
        self.name=name
        
trainingset =[DecisionTree(m.monk1,"monk1TrainingData"),
              DecisionTree(m.monk2,"monk2TrainingData"),
              DecisionTree(m.monk3,"monk3TrainingData")]

testset = [DecisionTree(m.monk1test,"monk1TestData"),
           DecisionTree(m.monk2test,"monk2TestData"),
           DecisionTree(m.monk3test,"monk3TestData")]

def calculateEntropyOfTrainingData():
        for set in trainingset:
           print("Entropy of "+set.name+" : "+str(d.entropy(set.dataset)))
        print("")
calculateEntropyOfTrainingData()

def calculateInformationGain():
    for set in trainingset:
        getAverageInformationGain(set.dataset,set.name)


def getAverageInformationGain(dataset,name):
    print("Information Gain of:"+name+":")
    for i in range (len(m.attributes)):
        print("InformationGain of "+name +" "+m.attributes[i].name+" : "+ str(d.averageGain(dataset,m.attributes[i])))
    print("The Best Attribute for splitting the result "+ name +":"+ str(d.bestAttribute(dataset,m.attributes)))
calculateInformationGain()

def splittingHighestAttribute():
     a5=m.attributes[4]
     for set in trainingset:
         for attibuteValues in a5.values:
             subset=d.select(set.dataset ,a5,attibuteValues)
             getAverageInformationGain(subset,set.name +"on A5 = "+str(attibuteValues))  
splittingHighestAttribute()

def buildTreeFromMonk1Data():
    for i in range(len(trainingset)-2):
        tree= d.buildTree(trainingset[i].dataset, m.attributes, maxdepth=3)
        qt.drawTree(tree)
        
buildTreeFromMonk1Data()


def buildtree():
    for i in range(len(trainingset)):
        tree=d.buildTree(trainingset[i].dataset,m.attributes)        
        performanceOnTrainData = d.check(tree,trainingset[i].dataset)
        performanceOnTestData=d.check(tree,testset[i].dataset)
        print("Error of " + trainingset[i].name+ "on " + testset[i].name + ":" + str(1-performanceOnTestData))
        print("Error of " + trainingset[i].name+ "on " + trainingset[i].name + ":" + str(1-performanceOnTrainData))
        
        

buildtree()

def partition(data, fraction):
     ldata = list(data) 
     random.shuffle(ldata)
     breakPoint = int(len(ldata) * fraction)
     return ldata[:breakPoint], ldata[breakPoint:]

def prunedtree(data,fraction):
    trainset,validationSet=partition(trainingset,fraction)
    tree =d.buildTree(trainset,m.attributes)
    bestTreeSoFar =tree    
    bestPerformance=d.check(tree,validationSet)  
    print("Pruning"+trainset+ "and fraction ="+ str(fraction)+
    "and performance on new validationSet ="+ str(bestPerformance))
    return bestTreeSoFar,bestPerformance    

#     bestTreeSoFar= tree
#     bestPerformance=d.check(tree,validationSet)









 


    
       