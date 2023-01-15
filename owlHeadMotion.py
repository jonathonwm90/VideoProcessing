# owlHeadMotion.py VID_EDITED/filename
""""
Second argument in the cmd is the path of the video to be analyzed.
"""""
import sys

import cv2
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton

from geometry import *

global coors
coors = []
global coors2
coors2 = []

global name

in_file_name = sys.argv[1]
file_names = in_file_name.split("/")
name = file_names[-1].replace(".avi","")

def on_click(event):
    if event.button is MouseButton.LEFT:
        if len(coors) == 0:       
            coors.append([event.xdata, event.ydata])
            plt.close()
              
def on_click3(event):
    global coors2
    if event.button is MouseButton.LEFT:     
        coors2.append([event.xdata, event.ydata])

        if len(coors2) == 3:
            plt.close()

        if len(coors2) == 4:
            coors2 = [[event.xdata, event.ydata]]
    
def get_closest(points, targetPoint):
    distances = []

    for i in range(len(points[0])):
        dist = get_distance((points[0][i], points[1][i]), (targetPoint[0][0], targetPoint[0][1]))
        distances.append(dist)

    mini = min(distances)
    index = distances.index(mini)

    return index

def format_contour(x: int, contours: list):# gets the (x,y) coordinates for the desired contour, and plots it
    formatted_contours = []
    for i in range(len(contours[x])):
        formatted_contours.append(contours[x][i][0])
    
    xvars, yvars = [], []
    for i in range(len(formatted_contours)):
        xvars.append(formatted_contours[i][0])
        yvars.append(formatted_contours[i][1])

    return xvars, yvars

def get_contour_center(y, contours_list, centers = [[],[]]): # gets the center of the desired contour number (in list of contours), y
    contour1 = []
    contour1 = format_contour(y, contours_list)

    contour1[0].sort()
    contour1[1].sort()

    x_ave = 0
    y_ave = 0

    x_ave = (contour1[0][0] + contour1[0][-1])/2 # finds the average of the extreems of x and y
    y_ave = (contour1[1][0] + contour1[1][-1])/2

    centers[0].append(x_ave)
    centers[1].append(y_ave)

    return x_ave, y_ave, contour1

def get_first_contour(frame, contours):
    bad_centers = [[],[]]
    centers = [[],[]]
    base_center = [0,0]

    old_x = 0
    old_y = 0

    counter = 1

    for i in contours:
        x, y, thing = get_contour_center(0, [i], bad_centers)        

        if abs(old_x - x) < 5:
            continue
                    
        if abs(old_y - y) < 5:
            continue

        old_x = x
        old_y = y
        counter += 1

        centers[0].append(x)
        centers[1].append(y)

    plt.figure(figsize=(7,7))
    plt.connect('button_press_event', on_click)
    plt.scatter(centers[0], centers[1], marker='.', color='r')
    plt.imshow(frame)
    plt.show()

    index = get_closest(centers, coors)

    base_center[0] = centers[0][index]
    base_center[1] = centers[1][index]
    return base_center

def check_contours(x_range, y_range, contours, previous_center, counter):
    #global last_good_center #y_range and x_range are the max distance the points can be from each other on respective axis
    centers = [[],[]]
    good_centers = [[],[]]

    for i in range(len(contours)):
        x_cent, y_cent, contour = get_contour_center(i, contours)
        centers[0].append(x_cent)
        centers[1].append(y_cent)
        
    for i in range(len(centers[0])):
        if (abs(centers[0][i] - previous_center[0])) < (x_range) and (abs(centers[1][i] - previous_center[1])) < (y_range):
            good_centers[0].append(centers[0][i])
            good_centers[1].append(centers[1][i])
        #elif (abs(centers[0][i] - last_good_center[0])) < (x_range) and (abs(centers[1][i] - last_good_center[1])) < (y_range):
        #    good_centers[0].append(centers[0][i])
        #    good_centers[1].append(centers[1][i])
        

    if len(good_centers[0]) >= 2:
        counter += 1
        return [good_centers[0][1]], [good_centers[1][1]], counter
        
    elif len(good_centers[0]) == 0 or len(good_centers[1]) == 0:
        #last_good_center = previous_center
        #print("previous_center used")
        return previous_center[0], previous_center[1], counter
    else:
        return good_centers[0], good_centers[1], counter

def get_video_centers(video: str): #plays the video and returns centers and the capture object
    cap_centers = [[],[]]
    
    cap = cv2.VideoCapture(video) #sys.argv[1]

    counter = 0
    frames = 0

    while (cap.isOpened()):
        ret, frame = cap.read()
        
        if ret == True:            
            canny = cv2.Canny(frame, 50, 265) #70, 420
            #                                 ^    ^
            #                 change these    |    |  to change contour finding
            contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) == 0:
                continue

            if frames == 0:
                global start_frame
                start_frame = frame
                cv2.imwrite(f"PicOutputs/{name}_image.jpg", start_frame)
                base_center = get_first_contour(frame, contours)
                #global last_good_center
                #last_good_center = base_center

            x_c, y_c, counter = check_contours(20, 10, contours, base_center, counter)

            if x_c != 0 or y_c != 0: 
                base_center = [x_c, y_c]
                cap_centers[0].append(x_c)
                cap_centers[1].append(y_c)

            scale_percent = 90 # percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            
            cv2.drawContours(frame, contours, -1 ,(0,255,0), 2)
            resized = cv2.resize(frame, dsize=(width, height))
            cv2.imshow("objects Found", resized)
            cv2.resizeWindow("objects Found", width, height)
            
            frames += 1

        else:
            break

        if cv2.waitKey(25) == ord('q'): #not sure what this does, but you need it.
            break
    cap.release()
    return cap_centers, cap, counter

vid_centers1, capture, num_exc = get_video_centers(sys.argv[1])
vid_centers = []

for i in vid_centers1:
    if i not in vid_centers:
        vid_centers.append(i)

print(f"There were {num_exc} times when two points were found in the constraints for the next point\a")
cv2.destroyAllWindows()

minx = min(vid_centers[0])
indxm = vid_centers[0].index(minx)
minp = (vid_centers[0][indxm], vid_centers[1][indxm])

maxx = max(vid_centers[0])
indxmax = vid_centers[0].index(maxx)
maxp = (vid_centers[0][indxmax], vid_centers[1][indxmax])

def try_circle(start_frame, vid_centers, name):
    plt.figure(figsize = (8,8))
    plt.imshow(start_frame)
    plt.plot(vid_centers[0], vid_centers[1], color="blue", marker=".", zorder=2, label='Head Movement')
    plt.legend(loc="upper right")
    plt.connect("button_press_event", on_click3)
    plt.show()
    
    cx, cy, radius = get_circle(coors2[0], coors2[1], coors2[2])
    #startframe, vid_centers, name

    plt.figure(figsize = (8,8))
    plt.imshow(start_frame)
    plt.plot(vid_centers[0], vid_centers[1], color="blue", marker=".", zorder=2, label='Head Movement')
    plt.scatter(cx, cy, color='red', zorder=1, label="center of rotation")
    plt.legend(loc="upper right")
    circle = plt.Circle((cx, cy), radius, fill = False, zorder=3, color="red")
    plt.gca().add_patch(circle)
    plt.savefig(f"Plots/{name}.png")
    plt.show()
    return cx, cy

cx, cy = try_circle(start_frame, vid_centers, name)
is_good = input("was that good, y or n: ")
while is_good == 'n':
    cx, cy = try_circle(start_frame, vid_centers, name)
    is_good = input("was that good, y or n: ")

with open(f"TextOutputs/{name}_output.txt", "w") as file:
    file.write(f"{str(cx)} {str(cy)}\n{str(minp[0][0])} {str(minp[1][0])}\n{str(maxp[0][0])} {str(maxp[1][0])}\n")
    for i in range(len(vid_centers[0])):
        file.write(f"{str(vid_centers[0][i][0])} {str(vid_centers[1][i][0])}\n")