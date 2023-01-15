import matplotlib.pyplot as plt
import cv2
import os
from matplotlib.backend_bases import MouseButton
import geometry as gy
import Lasso as ls

global coors
coors = []

def on_click(event):
    if event.button is MouseButton.LEFT:
        if len(coors) == 0:       
            coors.append([event.xdata, event.ydata])
            plt.close()

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
            CenterOfRot = [float(line[0]), float(line[1])]
        elif i == 1 or i == 2:
            pass
        else:
            movement[0].append(float(line[0]))
            movement[1].append(float(line[1]))

    plt.connect("button_press_event", on_click)
    plt.plot(movement[0], movement[1])
    plt.scatter(CenterOfRot[0], CenterOfRot[1], color='r')
    name2 = formattedNames[filesList.index(fileContents)]
    print(name2)
    picture = cv2.imread(f"PicOutputs/{name2}_image.jpg")
    plt.imshow(picture)
    plt.show()

    radius = gy.get_distance(coors[0], CenterOfRot)
    
    plt.plot(movement[0], movement[1])
    plt.scatter(CenterOfRot[0], CenterOfRot[1], color='r')
    circle = plt.Circle((CenterOfRot[0], CenterOfRot[1]), radius, fill = False, zorder=3, color="red")
    plt.gca().add_patch(circle)
    plt.imshow(picture)
    plt.savefig(f"PlotsEdited/{name2}.png")
    plt.show()

    
    coors = []