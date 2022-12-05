import sys
import geometry as gy
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import cv2

global coors
coors = []

def on_click(event):
    if event.button is MouseButton.LEFT:
        if len(coors) < 2:
            coors.append((event.xdata, event.ydata))
        if len(coors) == 2:
            plt.close()

def convert(num, ratio):
    return num * ratio

def plot_line_dist(image, point1, point2, ratio, **args):
    uc_dist = gy.get_distance(point1, point2)
    distance = convert(uc_dist, ratio)
    plt.plot((point1[0], point2[0]), (point1[1], point2), color="red", label=f'{distance}', marker='.')
    plt.imshow(image)
    plt.legend(loc="upper right")

with open(f"TextOutputs/{sys.argv[1]}_output.txt", 'r') as file:
    text = file.readlines()

L1_text_split = text[0].split(" ")
min_text = text[1].split(" ")
max_text = text[2].split(" ")

x_center, y_center = float(L1_text_split[0]), float(L1_text_split[1])
minpt = (float(min_text[0]), float(min_text[1]))
maxpt = (float(max_text[0]), float(max_text[1]))

image = cv2.imread(f"PicOutputs/{sys.argv[1]}_image.jpg")

print("first two clicks are for the known distance")

plt.figure(figsize=(7,7))
plt.connect("button_press_event", on_click)
plt.plot(x_center, y_center, color="red", marker='o')
plt.imshow(image)
plt.show()

point1 = coors[0]
point2 = coors[1]
  
distance_inpt = gy.get_distance(point1, point2)

given_dist = float(input("Input the known distance:\n"))

ratio = given_dist/distance_inpt

plot_line_dist(image, point1, [x_center, y_center], ratio, color='b')
plot_line_dist(image, point2, [x_center, y_center], ratio, color='r')
plt.show()