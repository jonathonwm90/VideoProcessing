import matplotlib.pyplot as plt
import cv2
import os
import sys
from matplotlib.backend_bases import MouseButton
import geometry as gy

global coors
global coors2
coors = []
coors2 = []

def on_click2(event):
    if event.button is MouseButton.LEFT:
        if len(coors2) < 2:
            coors2.append((event.xdata, event.ydata))
        if len(coors2) == 2:
            plt.close()

def on_click(event):
    if event.button is MouseButton.LEFT:
        if len(coors) == 0:       
            coors.append([event.xdata, event.ydata])
            plt.close()

def convert(num, ratio):
    return num * ratio

def plot_line(image, line: gy.Line, color, angle):
    plt.plot((line.coor1[0], line.coor2[0]), (line.coor1[1], line.coor2[1]), color=color, marker='.', label=f'{angle} \u00b0')
    plt.imshow(image)




name2 = str(sys.argv[1])
image = cv2.imread(f"PlotsEdited/{name2}")

plt.connect("button_press_event", on_click)
plt.imshow(image)
plt.show()

COR = coors[0]
coors = []

plt.connect("button_press_event", on_click)
plt.imshow(image)
plt.show()

radius = gy.get_distance(coors[0], COR)

plt.connect("button_press_event", on_click2)
plt.imshow(image)
plt.show()

point1 = coors2[0]
point2 = coors2[1]

line1 = gy.Line(point1, COR)
line2 = gy.Line(point2, COR)

line1.get_m_b()
line2.get_m_b()

angle1 = round(gy.get_angle_to_vertical(line1), 2)
angle2 = round(gy.get_angle_to_vertical(line2), 2)

angle = round(angle1+angle2, 2)


plt.scatter(COR[0], COR[1], color='r')
plt.plot((COR[0], COR[0]), (COR[1], COR[1]-radius), color='purple', marker='.')
plot_line(image, line1, 'r', angle1)
plt.legend(loc="upper left")
plot_line(image, line2, 'b', angle2)
plt.legend(loc="upper right")
plt.savefig(f"AnglePlots/{name2}")
plt.show()
