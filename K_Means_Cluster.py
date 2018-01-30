from numpy import *
from random import *

def RandomSeletion(K,M):
    randomlist = []
    while len(randomlist) < K:
        randomnumber = randint(0,M-1)
        if randomnumber not in randomlist:
            randomlist.append(randomnumber)
    return randomlist

def Classification(X,K,C,ClassifiedX):
    if not X:
        return None
    ClassifiedX[C[0]].append(list(X[0]))
    Classification(X[1::],K,C,ClassifiedX)

class KMeansCluster(object):
    def __init__(self,X,K,times):
        self.X = X
        self.K = K
        self.Initialization()
        for time in range(times):
            self.ClusterAllocation()
            self.ClusterCentroidMove()
        self.cost = self.CostFunction()
    def Initialization(self):
        self.U = array([self.X[i] for i in RandomSeletion(self.K,len(self.X))])
        return None
    def ClusterAllocation(self):
        self.C = []
        for sample in self.X:
            distancelist = [inner((sample - clustercentroid),(sample - clustercentroid)) for clustercentroid in self.U]
            self.C.append(distancelist.index(min(distancelist)))
        return None
    def ClusterCentroidMove(self):
        ClassifiedX = []
        for i in range(self.K):
            ClassifiedX.append([])
        Classification(self.X,self.K,self.C,ClassifiedX)
        for j in range(len(ClassifiedX)):
            if not ClassifiedX[j]:
                self.K -= 1
                del ClassifiedX[j]
        self.U = array([array(list(map(sum,zip(*array(ClassifiedX[i])))))/len(ClassifiedX[i])\
                        for i in range(len(ClassifiedX))])
        return None
    def CostFunction(self):
        return sum([inner((self.X[i] - self.U[self.C[i]]),(self.X[i] - self.U[self.C[i]])) for i in range(len(self.X))])\
               /len(self.X)
