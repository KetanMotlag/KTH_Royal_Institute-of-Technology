from algorithm_abstract import Algorithm
from euclidian_heuristic import EucliHeur
import math
import numpy as np

class AStar(Algorithm):
    # Assumption: state = (id,prim,x,y,r,F,g)

    #Static Flags
    SOLUTION_FOUND = 0
    GOAL_FOUND = 1
    NO_SUCC = 2
    SUCC = 3
    UNDISCOVERED = 4
    DISCOVERED = 5
    FALIURE = 6

    #STATE
    isSolutionFound = False

    def __init__(self, boundary, start, goal, obstacles, space_resolution, stepFunction,
     primitives=90, primitive_bounds=[-math.pi/4.0, math.pi/4.0], rounding=8):

        #Abstract Variables
        self.OPEN = []
        self.CLOSE = []
        self.Boundry = boundary
        self.Start = start
        self.Goal = goal
        self.Obstacles = obstacles
        self.Res = space_resolution
        self.Path = {}

        #Heuristic Functions
        self.Heur = EucliHeur(self.Start, self.Goal, self.Obstacles)

        #Abstract Distance Function
        self.DFunc = self.Heur.getDistance

        #Class Variables
        #self.StateSpace = []
        self.StepFunc = stepFunction
        self.NumPrimitives = primitives
        self.PrimBounds = primitive_bounds
        self.Primitives = self.GetPrimitives(self.NumPrimitives, self.PrimBounds)
        self.Rounding = rounding

        print("Primitives: {}".format(self.Primitives))


    #--Overwrite Functions--

    def getNext(self):
        n = None
        while True:
            n = self.OPEN.pop(0)
            if not self.isDiscivered(n) or len(self.OPEN) == 0:
                break
        self.CLOSE.append(self.MakePoint(n))

        if self.isGoal(n):
            return AStar.GOAL_FOUND, n
        else:
            return AStar.UNDISCOVERED, n
       
    def updateFCost(self, n):
        n[6] += self.Heur.getFixedCost()
        n[5] = self.Heur.getHeuristic(n) + n[6]
        return n[5], n[6]

    def Expand(self, n):
        succs = []
        for prim in self.Primitives:
            nx, ny, tn = self.StepFunc(n[2]+self.Res,n[3]+self.Res,n[4],prim)
            state = [n[0], prim, nx, ny, tn, 0, n[6]]
            if self.isInLimits(state) and (not self.isDiscivered(state)):
                state[5], state[6] = self.updateFCost(state)
                succs.append(state)
                # print("Succ: ({},{},{},{}) => ({},{},{}) H: {}".format(n[2],n[3],n[4],prim, nx,ny,tn, state[5]))
            # else:
            #     if not self.isInLimits(state):
            #         print("Succs notin bound: {}".format(state))
            #     elif(self.isDiscivered(state)):
            #         print("Succs discovered: {}".format(state))

        if len(succs) == 0:
            return False, succs
        else:
            return True, succs

    #--Class Functions--

    def isDiscivered(self, n):
        # p = self.MakePoint(n)
        # print("Checking {} => {} in {}".format(n,p,self.CLOSE))
        # return p in self.CLOSE
        return self.isInList(n,self.CLOSE)

    def MakePoint(self, n):
        # return ( round(n[2],self.Rounding), round(n[3],self.Rounding), round(n[4],self.Rounding))
        return n
        
    # def StorePoint(self, n):
    #     self.StateSpace.append(self.MakePoint(n))

    # def ScaleState(self, n):
    #     return round((self.DFunc(n, [0,0]))/self.Res, 4)

    def GetPrimitives(self, num_of_primitives, bounds):
        return np.linspace(bounds[0],bounds[1],num_of_primitives)

    def Reconstruct(self):
        path = []
        key = self.getLastId()
        while key > 0:
            data = self.Path[key]
            path.append(data[1])
            key = data[0]
        return path

    def ExpansionConstruct(self):
        path = []
        for key in self.Path.keys():
            path.append(self.Path[key][1])
        return path

    def run(self):
        
        AStar.isSolutionFound = False
        
        self.Start[5] = self.Heur.getHeuristic(self.Start)
        self.Start[0] = self.getNewId()
        self.Start[1] = 0.0
        self.OPEN.append(self.Start)

        itr = 0

        while(not AStar.isSolutionFound):
            print("Iterations: {}".format(itr))
            itr +=1

            if (not len(self.OPEN)>0):
                print("OPEN Empty")
                break
            elif( itr > 500):
                print("Max States Expanded")
                break

            status, state = self.getNext()
            new_id = self.getNewId()
            self.Path[new_id] = [state[0], state[1]]
            state[0] = new_id
            
            if status == AStar.GOAL_FOUND:
                print("Goal found!")
                AStar.isSolutionFound = True
                break
            elif status == AStar.DISCOVERED:
                print("Discovered State Found")
                continue
            elif status == AStar.FALIURE:
                print("Faliure")
                break

            # print("Expanding: {} From: {}".format(state, self.OPEN))
            succ_exist, succs = self.Expand(state)
            if not succ_exist:
                print("No Successor Found")
                continue
            
            for s in succs:
                # s[6] += self.Heur.getFixedCost()

                # if(self.isInList(s, self.OPEN)):
                #     # print("{} exists in OPEN".format(s))
                #     isFound, element = self.getFromList(s, self.OPEN)
                #     if isFound:
                #         self.OPEN.pop(element)
                self.OPEN.append(s)

            self.sortList(self.OPEN)
            # print("OPEN: {}".format(self.OPEN))
        
        if AStar.isSolutionFound:
            return self.Reconstruct()
        else:
            return self.ExpansionConstruct()
        


