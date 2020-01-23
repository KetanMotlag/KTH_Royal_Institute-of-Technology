#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# {Ketan Motlag}
# {student id}
# {motlag@kth.se}

import random
from random import *
import math
from math import *
from numpy import *

from dubins import Car

car = Car()

def solution(car):

    initial_node = NodePoints(car.x0, car.y0, 0.0, 0.1)
    Goal_node = NodePoints(car.xt, car.yt, 0, 0)
    controls,times = node_generation(initial_node,Goal_node,car.xlb,car.xub,car.ylb,car.yub,car.obs)

    return controls, times


class NodePoints(self,x,y.theta,phi):
    def __init__(self,x,y,theta,phi):
        self.x=x
        self.y=y
        self.theta=theta
        self.phi=phi
        self.parent_node=None

def node_generation(int_node,end_node,car_xl,car_xu,car_yl,car_yu,car_obs):
    counter = 0
    nodelist = [int_node]
    while True:
        random = [uniform(0.0,20.0) , uniform(0.0,10.0)]
        counter = counter + 1
        if counter == 15:
            random = [end_node.x,end_node.y]
            counter = 0

        nearest_Node = get_nearest_node(random,nodelist)

        V = [cos(nearest_node.theta),sin(nearest_node.theta)]
        Rg = [(random[0] - nearest_Node.x),(random[1] - nearest_Node.y)]
        phi = steering_angle(V,Rg)
        xl = [nearest_Node.x]
        yl = [nearest_Node.y]
        thetal = [nearest_Node.theta]
        while incr <= 1:
            xn , yn , thetan = car.step(xl[-1],yl[-1],thetal[-1],phi)
            xl.append(xn)
            yl.append(yn)
            thetal.append(thetan)
            incr = incr + 0.01 #the increments that the car.step function works by
        if collision(xn,yn,car_obs) == False:
            new_Node = NodePoints(xn,yn,thetan,phi)
            new_Node.parent = nearest_Node
            nodelist.append(new_Node)
            if distance(new_Node.x,new_Node.y,Goal_node.x,Goal_node.y) <= 0.5:
                print("Goal Reached!")
                break
    last_index = len(nodelist) - 1
    controls = []
    while nodelist[last_index].parent != None:
        controls.append(nodelist[last_index].phi)
        last_index = last_index - 1

    controls.reverse()
    times = range(0,(len(controls)+1),1)

    return controls, times

def get_nearest_node(random,nodelist):
    d_list = [(sqrt((random[0] - node.x)**2 + (random[1] - node.y)**2)) for node in nodelist]
    n_node = nodelist[d_list.index(min(d_list))]
    return n_node

def steering_angle(V,Rg):
    V = array(V[0],V[1],0)
    Rg = array(Rg[0],Rg[1],0)
    angle = (dot(V,Rg))/( (norm(V))*(norm(Rg)) )
    direction = (dot(cross(V,Rg)),[0,0,1])/( (norm(V))*(norm(Rg)) )
    if angle < -0.25*pi:
        angle = -0.25*pi
    if angle > 0.25*pi:
        angle = 0.25*pi
    if direction >0:
        angle = angle
    if direction < 0:
        angle = -angle
    return angle

def distance(x1,y1,x2,y2):
    d = sqrt((x2-x1)**2 + (y2-y1)**2)
    return d

def collision(x,y,obs):
    for(obsx,obsy,obsr) in obs:
        d = distance(x,y,obsx,obsy)
        if x < 0.0 or x > 20.0 or y < 0.0 or y > 10.0:
            return True #collision occured
        if obsr == 0.2:
            if d <= 0.8:
                print("Collision")
                return True
        elif d<= 1.5*obsr:
            print("Collision")
            return True
    return False

if __name__ == '__main__':

    return controls, times
