# y = mx + b
import math
import matplotlib.pyplot as plt
class Line():
    def __init__(self, coor1 = (0,0), coor2 = (0,0), m = 0, b = 0):
        self.coor1 = coor1
        self.coor2 = coor2

        self.x1 = coor1[0]
        self.y1 = coor1[1]
        self.x2 = coor2[0]
        self.y2 = coor2[1]

        self.m = m
        self.b = b

    def get_m_b(self):
        if self.m == 0:
            self.m = float((self.y1 - self.y2)/(self.x1 - self.x2))
            
        if self.b == 0:
            self.b = float(self.y1 - (self.m * self.x1))

        return self.m , self.b

    def get_midpoint(self):
        x = ((self.x1 + self.x2) / 2)
        y = ((self.y1 + self.y2) / 2)
        self.midpoint = (x, y)
        return self.midpoint

def get_perpendicular_bisector(line):
    perp_slope = (-1) * (1 / line.m)
    mdpt = line.get_midpoint()
    perp_bisector = Line(coor1 = mdpt, m = perp_slope)
    perp_bisector.get_m_b()
    return perp_bisector

def get_intersection(line1, line2):
    b1 = line1.b
    b2 = line2.b
    m1 = line1.m
    m2 = line2.m
    x = (b1-b2)/(m2-m1)
    y_test1 = (line1.m * x) + line1.b
    y_test2 = (line2.m * x) + line2.b

    if abs(int(y_test1) - int(y_test2)) > 3:
        print("error occured: line intersections did not match up")
        return(0,0)
    else: 
        return (x, y_test1)

def get_distance(coor1, coor2):
    x1, y1 = coor1[0], coor1[1]
    x2, y2 = coor2[0], coor2[1]

    xDist = x2 - x1
    yDist = y2 - y1
    
    xd2 = xDist ** 2
    yd2 = yDist ** 2
    finDist = math.sqrt(xd2 + yd2)
    return finDist  

def get_circle(coor1, coor2, coor3):
    line1 = Line(coor1, coor2)
    line2 = Line(coor1, coor3)

    line1.get_m_b()
    line2.get_m_b()

    line3 = get_perpendicular_bisector(line1)
    line4 = get_perpendicular_bisector(line2)

    inter = get_intersection(line3, line4)

    cx, cy = inter[0], inter[1]
    r = get_distance(inter, coor3)

    return cx, cy, r