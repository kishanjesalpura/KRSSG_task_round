import cv2 as cv
import numpy as np
import random
import sys
import math

STEP_LENGTH = 30

class Node():
    def __init__(self, x, y, parent = None, path_cost = 0):
        self.x = x
        self.y = y
        self.parent = parent
        self.path_cost = path_cost


class Map():
    def __init__(self, map_array, start_node):
        self.map = map_array
        self.nodes = [start_node]
        self.maph, self.mapw, self.channels = self.map.shape

    def check_obstacles(self, node1, node2):
        d = abs(node1[0] -node2[0]) + abs(node1[1] - node2[1])
        path = np.linspace([node1[1], node1[0]], [node2[1], node2[0]], num = d, dtype = 'uint')
        for p in path:
            pixel = self.map[p[0]][p[1]]
            if (pixel>np.array([190,190,190])).all():
                return True

    def create_new_node(self):
        random_x = random.randrange(0, self.maph)
        random_y = random.randrange(0, self.mapw)

        # finding nearest node
        n_node = self.nodes[0]
        distance = abs(random_x - self.nodes[0].x) + abs(random_y - self.nodes[0].y)
        for node in self.nodes:
            d = abs(random_x - node.x) + abs(random_y - node.y)
            if d < distance:
                n_node = node
                distance = d
            if distance == 0:
                return 0

        # getting node coordinates
        nodex = n_node.x+int(((random_x-n_node.x)/distance)*STEP_LENGTH)
        nodey = n_node.y+int(((random_y-n_node.y)/distance)*STEP_LENGTH)
        if nodex<0:
            nodex = 0
        elif nodex>(self.mapw-1):
            nodex = self.mapw-1
        if nodey<0:
            nodey = 0
        elif nodey>(self.maph-1):
            nodey = self.maph-1


        # checking for obstacles in the path
        if self.check_obstacles((nodex, nodey), (n_node.x, n_node.y)):
            return 0

        # adding node to the list of nodes
        path_cost = abs(nodex-n_node.x) + abs(nodey-n_node.y)
        self.nodes.append(Node(nodex, nodey, n_node, n_node.path_cost+path_cost))
    
        # changing the tree wrt that node
        curr_node = self.nodes[-1]
        for n in self.nodes[:-1]:
            w = abs(n.x-curr_node.x)
            h = abs(n.y-curr_node.y)
            if w<3*STEP_LENGTH and h<3*STEP_LENGTH:
                if n.path_cost+w+h <= curr_node.path_cost:
                    if not self.check_obstacles((n.x,n.y), (curr_node.x,curr_node.y)):
                        curr_node.parent = n
                elif n.path_cost>=curr_node.path_cost+w+h:
                    if not self.check_obstacles((n.x,n.y), (curr_node.x,curr_node.y)):
                        n.parent = curr_node
    
def merge_maps(map1, map2):
    connections = []
    for s_node in map1.nodes:
        for e_node in map2.nodes:
            d = abs(s_node.x - e_node.x) + abs(s_node.y - e_node.y)
            if d <= STEP_LENGTH:
                r = Map(image).check_obstacles((s_node.x, s_node.y), (e_node.x, e_node.y))
                if not r:
                    connections.append((s_node, e_node))
    return connections

def print_merged_map(image, connections, map1, map2):
    best_conn = connections[0]
    d = abs(connections[0][0].x - connections[0][1].x) + abs(connections[0][0].y - connections[0][1].y)
    path_length = connections[0][0].path_cost + connections[0][1].path_cost + d
    for conn in connections:
        d = abs(conn[0].x - conn[1].x) + abs(conn[0].y - conn[1].y)
        tot_length = conn[0].path_cost + conn[1].path_cost + d
        if tot_length<path_length:
            best_conn = conn
            path_length = tot_length
    
    for n in best_conn:
        while n.parent is not None:
            cv.circle(image, (n.x, n.y), 5, color = [255,0,0], thickness = -1)
            cv.line(image, (n.x, n.y), (n.parent.x, n.parent.y), color = [255,0,0], thickness = 2)
            n = n.parent
    cv.line(image, (best_conn[0].x, best_conn[0].y), (best_conn[1].x, best_conn[1].y), color = (255,0,0), thickness = 2)
        
        
    cv.namedWindow("w", cv.WINDOW_NORMAL)
    cv.imshow("w", image)
    cv.waitKey(0)
    cv.destroyAllWindows()

def obstacle_optimise(img, robot_radius):
    image = img.copy()
    maph, mapw, channels = image.shape
    y,x = 0,0
    while y<maph:
        while x<mapw:
            if (image[y][x]>[200,200,200]).all():
                for xo in range(max(x-robot_radius,0), min(x+robot_radius,mapw)):
                    for yo in range(max(y-robot_radius,0), min(y+robot_radius,maph)):
                        image[yo][xo] = [199,199,199]
                x = x+robot_radius
            x+=1
        y+=1
        x = 0
    return image

def get_nodes(image, colour):
    s = np.array(colour - 20)
    e = np.array(colour + 20)
    binary = cv.inRange(image, s, e)
    
    circles = cv.HoughCircles(binary, cv.HOUGH_GRADIENT, 1.5,10,param1=100,param2=1,minRadius=0,maxRadius=0)
    return circles

image = cv.imread("map2.png", 1)
image_optimised = obstacle_optimise(image, 10)
start = get_nodes(image.copy(), np.array([0,0,255]))
end = get_nodes(image.copy(), np.array([0,255,0]))
mapR1 = Map(image_optimised, start[0][:2])
mapR2 = Map(image_optimised, start[1][:2])
mapR3 = Map(image_optimised, start[2][:2])
mapG1 = Map(image_optimised, end[0][:2])
mapG2 = Map(image_optimised, end[1][:2])
mapG3 = Map(image_optimised, end[2][:2])


# map1 = Map(image_optimised)
# map1.start_node(0,255,0)
# map2 = Map(i1)
# map2.start_node(0,0,255)
# for _ in range (200):
#     r1 = map1.create_new_node()
#     r2 = map2.create_new_node()
#     while r1 == 0 or r2 == 0:
#         r1 = map1.create_new_node()
#         r2 = map2.create_new_node()
# conns = merge_maps(map1, map2)
# print_merged_map(i2, conns, map1, map2)

