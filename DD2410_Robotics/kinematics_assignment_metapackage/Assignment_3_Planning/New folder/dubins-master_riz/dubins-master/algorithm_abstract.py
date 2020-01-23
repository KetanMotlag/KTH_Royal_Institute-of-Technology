
class Algorithm:
    OPEN = []
    CLOSE = []

    Boundry = [[], []]

    Start = []
    Goal = []

    Obstacles = []

    #Resolution of environment = smallest obstacle radius
    Res = 0.0

    #Distance Function
    DFunc = None

    #Reconstruct Path
    Path = {} # Path[id] = [parent_id, value]

    #Path ids
    id = -1

    def getLastId(self):
        return self.id

    def getNewId(self):
        self.id += 1
        return self.id

    def isOpenEmpty(self):
        if (len(self.OPEN) == 0):
            return True
        else:
            return False

    def isGoal(self, n):
        if (self.DFunc(n, self.Goal) <= self.Res):
            return True
        else:
            return False

    def sortList(self, l):
        l.sort(key=lambda x: x[5])

    def isInLimits(self, n):
        if (n[2] >= self.Boundry[0][0] and n[3] >= self.Boundry[0][1]):
            if (n[2] <= self.Boundry[1][0] and n[3] <= self.Boundry[1][1]):
                return True
        return False

    def isInList(self, n, li):
        for i in range(len(li)):
            if (self.DFunc(li[i], n) <= self.Res):
                return True
        return False

    def getFromList(self, n, li):
        for i in range(len(li)):
            if (self.DFunc(li[i], n) <= self.Res):
                return True, i
        return False, 0

    #Abstract
    def getNext(self):
        raise NotImplementedError("Please Implement this method");

    def updateFCost(n):
        raise NotImplementedError("Please Implement this method");

    def Expand(n):
        raise NotImplementedError("Please Implement this method");


