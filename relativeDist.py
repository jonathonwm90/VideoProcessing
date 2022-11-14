import sys
import geometry
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import cv2

global coors
coors = []

def on_click(event):
    if event.button is MouseButton.LEFT:
        if len(coors) < 3:
            coors.append((event.xdata, event.ydata))
            print(f'You pressed at: ({event.xdata}, {event.ydata})')

with open(f"TextOutputs/{sys.argv[1]}_output.txt", 'r') as file:
    text = file.readline()

texts = text.split(" ")
x_center, y_center = float(texts[0]), float(texts[1])

image = cv2.imread(f"PicOutputs/{sys.argv[1]}_image.jpg")

plt.figure(figsize=(7,7))
plt.connect("button_press_event", on_click)

plt.plot(x_center, y_center, color="red", marker='o')
plt.imshow(image)

plt.show()
print("\n", coors)
