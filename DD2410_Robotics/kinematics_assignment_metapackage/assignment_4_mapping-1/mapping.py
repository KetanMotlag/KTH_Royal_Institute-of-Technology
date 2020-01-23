#!/usr/bin/env python3

"""
    # {Hendrik Jan Loeffel}
    # {19941128T398}
    # {loffel@kth.se}
"""

# Python standard library
from math import cos, sin, atan2, fabs, sqrt

# Numpy
import numpy as np

# "Local version" of ROS messages
from local.geometry_msgs import PoseStamped, Quaternion
from local.sensor_msgs import LaserScan
from local.map_msgs import OccupancyGridUpdate

from grid_map import GridMap


class Mapping:
    def __init__(self, unknown_space, free_space, c_space, occupied_space,
                 radius, optional=None):
        self.unknown_space = unknown_space
        self.free_space = free_space
        self.c_space = c_space
        self.occupied_space = occupied_space
        self.allowed_values_in_map = {"self.unknown_space": self.unknown_space,
                                      "self.free_space": self.free_space,
                                      "self.c_space": self.c_space,
                                      "self.occupied_space": self.occupied_space}
        self.radius = radius
        self.__optional = optional

    def get_yaw(self, q):
        """Returns the Euler yaw from a quaternion.
        :type q: Quaternion
        """
        return atan2(2 * (q.w * q.z + q.x * q.y),
                     1 - 2 * (q.y * q.y + q.z * q.z))

    def raytrace(self, start, end):
        """Returns all cells in the grid map that has been traversed
        from start to end, including start and excluding end.
        start = (x, y) grid map index
        end = (x, y) grid map index
        """
        (start_x, start_y) = start
        (end_x, end_y) = end
        x = start_x
        y = start_y
        (dx, dy) = (fabs(end_x - start_x), fabs(end_y - start_y))
        n = dx + dy
        x_inc = 1
        if end_x <= start_x:
            x_inc = -1
        y_inc = 1
        if end_y <= start_y:
            y_inc = -1
        error = dx - dy
        dx *= 2
        dy *= 2

        traversed = []
        for i in range(0, int(n)):
            traversed.append((int(x), int(y)))

            if error > 0:
                x += x_inc
                error -= dy
            else:
                if error == 0:
                    traversed.append((int(x + x_inc), int(y)))
                y += y_inc
                error += dx

        return traversed

    def add_to_map(self, grid_map, x, y, value):
        """Adds value to index (x, y) in grid_map if index is in bounds.
        Returns weather (x, y) is inside grid_map or not.
        """
        if value not in self.allowed_values_in_map.values():
            raise Exception("{0} is not an allowed value to be added to the map. "
                            .format(value) + "Allowed values are: {0}. "
                            .format(self.allowed_values_in_map.keys()) +
                            "Which can be found in the '__init__' function.")

        if self.is_in_bounds(grid_map, x, y):
            grid_map[x, y] = value
            return True
        return False

    def is_in_bounds(self, grid_map, x, y):
        """Returns weather (x, y) is inside grid_map or not."""
        if x >= 0 and x < grid_map.get_width():
            if y >= 0 and y < grid_map.get_height():
                return True
        return False

    def update_map(self, grid_map, pose, scan): 
        
        """Updates the grid_map with the data from the laser scan and the pose.
        
        For E: 
            Update the grid_map with self.occupied_space.

            Return the updated grid_map.

            You should use:
                self.occupied_space  # For occupied space

                You can use the function add_to_map to be sure that you add
                values correctly to the map.

                You can use the function is_in_bounds to check if a coordinate
                is inside the map.

        For C:
            Update the grid_map with self.occupied_space and self.free_space. Use
            the raytracing function found in this file to calculate free space.

            You should also fill in the update (OccupancyGridUpdate()) found at
            the bottom of this function. It should contain only the rectangle area
            of the grid_map which has been updated.

            Return both the updated grid_map and the update.

            You should use:
                self.occupied_space  # For occupied space
                self.free_space      # For free space

                To calculate the free space you should use the raytracing function
                found in this file.

                You can use the function add_to_map to be sure that you add  print(x)
                print(y)
                values correctly to the map.

                You can use the function is_in_bounds to check if a coordinate
                is inside the map.

        :type grid_map: GridMap
        :type pose: PoseStamped
        :type scan: LaserScan
        """

        # Current yaw of the robot
        robot_yaw = self.get_yaw(pose.pose.orientation)
        # The origin of the map [m, m, rad]. This is the real-world pose of the
        # cell (0,0) in the map.
        origin = grid_map.get_origin()
        # The map resolution [m/cell]
        resolution = grid_map.get_resolution()
        
        
        """
        print("das sind die Pose- Werte: " +str(pose))
       
        a = True
        if a == True:
            print("das sind die grid- Werte: " +str(grid_map)) 
            a = False
        """
        x_list = []
        y_list = []
        #x_y_list = []
        occupied_cells = []
        
        
        for i in range(len(scan.ranges)):
            
            if scan.ranges[i] > scan.range_min and scan.ranges[i] < scan.range_max:
                
                x = (scan.ranges[i] * cos(robot_yaw + (scan.angle_min + scan.angle_increment * i))) + pose.pose.position.x - origin.position.x
                
                y = (scan.ranges[i] * sin(robot_yaw + (scan.angle_min + scan.angle_increment * i))) + pose.pose.position.y - origin.position.y
                
                #x and y end index
                
                x = int(x / resolution) 
                y = int(y / resolution)
                
                occupied_cells.append([x,y])
 
                
                #mark as free
                
                starting_x = int((pose.pose.position.x - origin.position.x) / resolution)
                
                starting_y = int((pose.pose.position.y - origin.position.y) / resolution)    
                
                start = [starting_x, starting_y]
                
                end = [x,y]  
                                
                traversed = self.raytrace(start, end)
                
                
                for i in traversed:
                                        
                    self.add_to_map(grid_map, i [0], i [1],self.free_space)
                    
                    if self.is_in_bounds(grid_map, i[0], i[1]):
                                                                            
                        x_list.append(i[0])
                    
                        y_list.append(i[1])
                    
                        #x_y_list.append([i[0],i[1],self.free_space])                
                              
                
                #x and y end index add to list
                #x_list.append(x)
                
              
        #mark as occupied
        
        for i in range(len(occupied_cells)):
                          
            self.add_to_map(grid_map,occupied_cells [i][0], occupied_cells [i] [1],self.occupied_space)   
            
            #if self.is_in_bounds(grid_map,occupied_cells [i][0], occupied_cells [i][1]):
            
                #x_list.append(occupied_cells [i][0])
                
                #y_list.append(occupied_cells [i][1])
            
                #x_y_list.append([occupied_cells [i][0],occupied_cells [i][1],self.occupied_space])
                
        
        #x_y_list.sort()
                
        data = []
    
        # Only get the part that has been updated
        update = OccupancyGridUpdate()
        
        # The minimum x index in 'grid_map' that has been updated
        update.x = min(x_list)
                   
        # The minimum y index in 'grid_map' that has been updated
        update.y = min(y_list)
        
        # Maximum x index - minimum x index + 1
        update.width = max(x_list) - min(x_list) + 1
        #print("Breite des Rechtecks: " +str(update.width))
        
        # Maximum y index _map- minimum y index + 1
        update.height = max(y_list) - min(y_list) + 1
        
        #print("Hoehe des Rechtecks: " +str(update.height))
        # The map data inside the rectangle, in row-major order.
        
        for h in range(update.height):
            
            for i in range(update.width):
                
                data.append(grid_map[update.x + i, update.y + h])
                                
        update.data = data
        #print("das sind die Daten: " +str(data))
        
        return grid_map, update
   

    def inflate_map(self, grid_map):
        
        """For C only!
        Inflate the map with self.c_space assuming the robot
        has a radius of self.radius.
        
        Returns the inflated grid_map.

        Inflating the grid_map means that for each self.occupied_space
        you calculate and fill in self.c_space. Make sure to not overwrite
        something that you do not want to.
        

        You should use:
            self.c_space  # For C space (inflated space).
            self.radius   # To know how much to inflate.

            You can use the function add_to_map to be sure that you add
            values correctly to the map.

            You can use the function is_in_bounds to check if a coordinate
            is inside the map.def is_in_bounds(self, grid_map, x, y):

        :type grid_map: GridMap
        
        """
        
     
        #print("Laenge Grid_ {}" .format(len(grid_map)))
              
        
        
        for i in range(grid_map.get_height()):
            
            for a in range(grid_map.get_width()):
                
                pos = [a,i]
                
                if grid_map.__getitem__(pos) == self.occupied_space:
                    
                                        
                    for y in range(i-3, i+4):
                        
                        for x in range(a-4, a+5):
                            
                            pos1 = [x,y]
                            
                            if self.is_in_bounds(grid_map,x,y) and grid_map.__getitem__(pos1) != self.occupied_space:
                                
                                self.add_to_map(grid_map, x,y,self.c_space)
                                
                           
                    for y in (i-4, i+4):
                                    
                        for x in range(a-3, a+4):
                                        
                            pos1 = [x,y]
                                        
                            if self.is_in_bounds(grid_map,x,y) and grid_map.__getitem__(pos1) != self.occupied_space and grid_map.__getitem__(pos1) != self.c_space :
                                            
                                self.add_to_map(grid_map, x,y,self.c_space) 
                                
                                
                   
                    for y in (i-5, i+5):
                        
                        x = a
                                        
                        pos1 = [x,y]
                                        
                        if self.is_in_bounds(grid_map,x,y) and grid_map.__getitem__(pos1) != self.occupied_space and grid_map.__getitem__(pos1) != self.c_space :
                                            
                            self.add_to_map(grid_map, x,y,self.c_space)
                                   
                    
                                     
                    for x in (a-5, a+5):
                        
                        y = i                
                        pos1 = [x,y]
                                        
                        if self.is_in_bounds(grid_map,x,y) and grid_map.__getitem__(pos1) != self.occupied_space and grid_map.__getitem__(pos1) != self.c_space :
                                            
                            self.add_to_map(grid_map, x,y,self.c_space)                   
                    
                               
                    
                   
      
        
        # Return the inflated map
        return grid_map
