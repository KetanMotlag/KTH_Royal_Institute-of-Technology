import math
import numpy as np
import random

class RRT():

    def __init__(self, boundary, start, goal, obstacles, space_resolution, stepFunction,
     primitives=90, primitive_bounds=[-math.pi/4.0, math.pi/4.0], rounding=8):
        
        self.epsilon = 0.1
        self.num_of_nodes = 5000

        self.Boundry = boundary
        self.Start = start
        self.Goal = goal
        self.Obstacles = obstacles

        self.StepFunc = stepFunction
        self.NumPrimitives = primitives
        self.PrimBounds = primitive_bounds
        self.Primitives = self.GetPrimitives(self.NumPrimitives, self.PrimBounds)
        self.Rounding = rounding

        self.id = -1

    def getCurrentId(self):
        return self.id

    def getNewId(self):
        self.id +=1
        return self.id

    def getDistance(self, n1, n2):
        x = (math.pow((n1[0] - n2[0]), 2)) + (math.pow((n1[1] - n2[1]), 2))
        return math.sqrt(x)

    def step(self,p1,p2):
        # if self.getDistance(p1,p2) <= self.epsilon:
        #     return None
        # else:
        #     theta = math.atan2(p2[1]-p1[1],p2[0]-p1[0])
        #     return p1[0] + self.epsilon*math.cos(theta), p1[1] + self.epsilon*math.sin(theta), theta

        phi = math.atan2(p2[1]-p1[1],p2[0]-p1[0])
        phi = p1[2]-phi
        
        # assert( (phi >= self.PrimBounds[0]) and (phi <= self.PrimBounds[1]) )
        if phi < self.PrimBounds[0]:
            phi = self.PrimBounds[0]
        elif phi > self.PrimBounds[1]:
            phi = self.PrimBounds[1]
        
        nx,ny,nt = self.StepFunc(p1[0], p1[1], p1[2], phi)
        return nx,ny,nt,phi


    def GetPrimitives(self, num_of_primitives, bounds):
        return np.linspace(bounds[0],bounds[1],num_of_primitives)

    def point2line(self, p1,p2):
        a = p2[1] - p1[1]
        b = p1[0] - p2[0]
        c = a*(p1[0]) + b*(p1[1])
        return a,b,c

    def checkCollision(self,a, b, c, x, y, radius):
        # Finding the distance of line 
        # from center.
        dist = ((abs(a * x + b * y + c)) /
                math.sqrt(a * a + b * b))
    
        # Checking if the distance is less 
        # than, greater than or equal to radius.
        if (radius == dist):
            # print("Touch")
            return True
        elif (radius > dist):
            # print("Intersect")
            return True
        else:
            # print("Outside")
            return False

    def isCollision(self, p1, p2):
        a,b,c = self.point2line(p1,p2)
        for ob in self.Obstacles:
            if self.checkCollision(a,b,c,ob[0],ob[1],ob[2]):
                return True
        return False

    def run(self):
        nodes = {} # nodes[id] = (x,y,theta,phi,id,parent)
        path = []

        nodes[0] = (self.Start[0], self.Start[1], 0.0, 0.0, self.getNewId(), -1) #(x,y,theta,phi,id,parent)

        for i in range(self.num_of_nodes):
            print("Iteration: {}".format(i))

            rand = (random.random()*self.Boundry[1][0], random.random()*self.Boundry[1][1])
            nn = nodes[0]
            for k in nodes.keys():
                p = nodes[k]
                if self.getDistance(p,rand) < self.getDistance(nn,rand):
                    nn = p
            nx, ny, nt, phi = self.step(nn, rand)
            newNode = (nx,ny,nt,phi,self.getNewId(),nn[4])
            if self.isCollision(nn, newNode):
                print("Collision Found")
                continue
            nodes[newNode[4]] = newNode
            print("NewNode: {}".format(newNode))

        
        # Check goal
        best_dist = 100000
        best_node = None
        for k in nodes.keys():
            node = nodes[k]
            dist_to_goal = self.getDistance(node, self.Goal)
            if dist_to_goal < best_dist:
                best_dist = dist_to_goal
                best_node = node
        
        nx, ny, nt, phi = self.step(best_node, self.Goal)
        finalNode = (nx,ny,nt,phi,self.getNewId(),best_node[4])
        nodes[finalNode[4]] = finalNode

        last_id = finalNode[4]
        while True:
            n = nodes[last_id]
            path.append(n[3])
            last_id = n[5]
            if last_id == -1:
                break

        return path


