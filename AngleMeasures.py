import matplotlib.pyplot as plt
import cv2
import os
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

fileNames = os.listdir("TextOutputs")

filesList = []
formattedNames = []

for name in fileNames:
    formattedNames.append(name.removesuffix("_output.txt"))
    with open(f"TextOutputs/{name}", "r") as file:
        filesList.append(file.readlines())

for fileContents in filesList:
    mov = [[],[]]
    for i in range(len(fileContents)):
        line = fileContents[i]
        line.removesuffix("\n")
        line = line.split(" ")

        if i == 0:  
            COR = [float(line[0]), float(line[1])]
        elif i == 1 or i == 2:
            pass
        else:
            mov[0].append(float(line[0]))
            mov[1].append(float(line[1]))

    name2 = formattedNames[filesList.index(fileContents)]
    image = cv2.imread(f"PicOutputs/{name2}_image.jpg")

    plt.connect("button_press_event", on_click)
    plt.plot(mov[0], mov[1])
    plt.scatter(COR[0], COR[1], color='r')
    plt.imshow(image)
    plt.title(f"{name2}")
    plt.show()

    radius = gy.get_distance(coors[0], COR)

    plt.connect("button_press_event", on_click2)
    circle = plt.Circle((COR[0], COR[1]), radius, fill = False, zorder=3, color="peru")
    plt.gca().add_patch(circle)
    plt.plot(mov[0], mov[1])
    plt.scatter(COR[0], COR[1], color='r')
    plt.imshow(image)
    plt.title(f"{name2}")
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

    circle = plt.Circle((COR[0], COR[1]), radius, fill = False, zorder=3, color="peru")
    plt.gca().add_patch(circle)
    plt.scatter(COR[0], COR[1], color='r')
    plt.plot((COR[0], COR[0]), (COR[1], COR[1]-radius), color='purple', marker='.')
    plot_line(image, line1, 'r', angle1)
    plt.legend(loc="upper left")
    plot_line(image, line2, 'b', angle2)
    plt.legend(loc="upper right")
    #plt.plot(mov[0], mov[1])
    plt.savefig(f"AnglePlots/{name2}.png")
    plt.show()





    coors2 = []
    coors = []