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

def plot_line_dist(image, point1, point2, ratio, col):
    uc_dist = gy.get_distance(point1, point2)
    distance = convert(uc_dist, ratio)
    distance = round(distance, 2)
    plt.plot((point1[0], point2[0]), (point1[1], point2[1]), col, label=f'{distance} mm', marker='.')
    plt.imshow(image)
    plt.legend(loc="lower left")

fileNames = os.listdir("TextOutputs")

filesList = []
formattedNames = []

for name in fileNames:
    formattedNames.append(name.removesuffix("_output.txt"))
    with open(f"TextOutputs/{name}", "r") as file:
        filesList.append(file.readlines())

for fileContents in filesList:
    movement = [[],[]]
    for i in range(len(fileContents)):
        line = fileContents[i]
        line.removesuffix("\n")
        line = line.split(" ")

        if i == 0:  
            COR = [float(line[0]), float(line[1])]
        elif i == 1 or i == 2:
            pass
        else:
            movement[0].append(float(line[0]))
            movement[1].append(float(line[1]))

    name2 = formattedNames[filesList.index(fileContents)]
    image = cv2.imread(f"PicOutputs/{name2}_image.jpg")

    plt.connect("button_press_event", on_click)
    plt.plot(movement[0], movement[1])
    plt.scatter(COR[0], COR[1], color='r')
    plt.imshow(image)
    plt.title(f"{name2}")
    plt.show()

    radius = gy.get_distance(coors[0], COR)

    circle = plt.Circle((COR[0], COR[1]), radius, fill = False, zorder=3, color="red")
    plt.gca().add_patch(circle)
    plt.connect("button_press_event", on_click2)
    plt.plot(movement[0], movement[1])
    plt.scatter(COR[0], COR[1], color='r')
    plt.imshow(image)
    plt.title(f"{name2}")
    plt.show()

    point1 = coors2[0]
    point2 = coors2[1]

    distance_inpt = gy.get_distance(point1, point2)

    given_dist = float(input("Input the known distance:\n"))

    ratio = given_dist/distance_inpt

    crossHead = gy.Line(point1, point2)
    crossHead.get_m_b()
    gy.get_perp_slope(crossHead)

    crossHeadPerp = gy.Line(coor1=COR, m=crossHead.perp_slope)
    crossHeadPerp.get_m_b()
    
    intersection = gy.get_intersection(crossHeadPerp, crossHead)
    circle = plt.Circle((COR[0], COR[1]), radius, fill = False, zorder=3, color="red")
    plt.gca().add_patch(circle)
    plot_line_dist(image, intersection, COR, ratio, col='g')
    plot_line_dist(image, point1, COR, ratio, col='b')
    plot_line_dist(image, point2, COR, ratio, col='r')
    plot_line_dist(image, point1, intersection, ratio, col="purple")
    plot_line_dist(image, point2, intersection, ratio, col="peru")
    #plt.plot(movement[0], movement[1])
    plt.savefig(f"DistancePlots/{name2}.png")
    plt.show()

    coors2 = []
    coors = []