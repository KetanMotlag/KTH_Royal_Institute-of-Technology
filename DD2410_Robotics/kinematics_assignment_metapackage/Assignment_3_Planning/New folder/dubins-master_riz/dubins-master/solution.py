#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Rizwan Asif
# 921008-8556
# rasif@kth.se

import math
# from Astar import AStar
from rrt import RRT

def solution(car):

    #boundary, start, goal, obstacles, space_resolution, stepFunction,
    #  primitives=5, primitive_bounds=[-math.pi/4.0, math.pi/4.0], rounding=4
    # Assumption: state = (id,prim,x,y,r,F,g)

    boundary = [[car.xlb,car.ylb],[car.xub,car.yub]]
    # start = [0,0,car.x0,car.y0,0,0,0]
    # gt = math.atan2(car.yt-car.y0, car.xt-car.x0)
    # goal = [-1,-1,car.xt,car.yt,gt,0,0]
    start = (car.x0,car.y0,0.0,0.0,0,0) #(x,y,theta,phi,id,parent)
    goal = (car.xt,car.yt,0.0,0.0,0,0)
    obstacles = car.obs
    #space_resolution = min(obstacles, key = lambda t: t[2])[2]/4.0 #smallest obstacle
    space_resolution = 0.01
    stepFunction = car.step

    print("Resolution: {}".format(space_resolution))
    print("Start: {}".format(start))
    print("Goal: {}".format(goal))
    print("Boundary {}".format(boundary))
    
    # astar = AStar(boundary, start, goal, obstacles, space_resolution, stepFunction)
    rrt = RRT(boundary, start, goal, obstacles, space_resolution, stepFunction)

    controls = [0,0,0]
    print("Started Planning")
    # controls = astar.run()
    controls = rrt.run()
    print("End Planning")

    assert(controls != None)

    times = [0]
    for _ in controls:
        times.append(times[-1]+car.dt)

    return controls, times


    # controls=[math.pi/4.0, math.pi/4.0, -math.pi/4.0]
    #times=[0,1,2,3]

    # # initial conditions
    # x = car.x0
    # y = car.y0
    # theta = 0.0
    # phi = 0.0
    # t = 0

    # phi1 = math.pi/4.0
    # phi2 = -math.pi/4.0
    # phi3 = math.pi/8.0

    # # numerical integration
    # xl, yl, thetal, phil, tl = [x], [y], [theta], [], [t]
    # while tl[-1] < 3:
    #     print("<--")
    #     xn, yn, thetan = car.step(xl[-1], yl[-1], thetal[-1], phi1)
    #     print("({}, {}, {}, {}) => ({}, {}, {})".format(xl[-1], yl[-1], thetal[-1], phi1,xn,yn,thetan))
    #     xn, yn, thetan = car.step(xl[-1], yl[-1], thetal[-1], phi2)
    #     print("({}, {}, {}, {}) => ({}, {}, {})".format(xl[-1], yl[-1], thetal[-1], phi2,xn,yn,thetan))
    #     xn, yn, thetan = car.step(xl[-1], yl[-1], thetal[-1], phi3)
    #     print("({}, {}, {}, {}) => ({}, {}, {})".format(xl[-1], yl[-1], thetal[-1], phi3,xn,yn,thetan))
    #     print("--->")
    #     xn, yn, thetan = car.step(xl[-1], yl[-1], thetal[-1], phi)
    #     print("({}, {}, {}, {}) => ({}, {}, {})".format(xl[-1], yl[-1], thetal[-1], phi,xn,yn,thetan))
    #     xl.append(xn)
    #     yl.append(yn)
    #     thetal.append(theta)
    #     phil.append(phi)
    #     tl.append(tl[-1] + car.dt)

    # return phil, tl
