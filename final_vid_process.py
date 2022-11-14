# final_vid_process.py VID_EDITED/side_head1.mp4 3
import statistics as stc
import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseButton

from geometry import *

plt.style.use('_mpl-gallery')

global coors
coors = []

def on_click(event):
    if event.button is MouseButton.LEFT:
        if len(coors) < 2 and len(coors) == 0:       
            coors.append([event.xdata, event.ydata])
            plt.close()
        
def get_closest(points, targetPoint):
    distances = []

    for i in range(len(points[0])):
        dist = get_distance(points[0][i], points[1][i], targetPoint[0][0], targetPoint[0][1])
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

def get_first_contour(frame, contours, another):
    bad_centers = [[],[]]
    centers = [[],[]]
    base_center = [0,0]
    
    old_x = 0
    old_y = 0

    global start_frame
    start_frame = frame

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

        if counter == len(contours):
            another = 1
            continue

        centers[0].append(x)
        centers[1].append(y)

    plt.figure(figsize=(7,7))
    plt.connect('button_press_event', on_click)
    plt.scatter(centers[0], centers[1])
    plt.imshow(frame)
    plt.show()

    index = get_closest(centers, coors)

    base_center[0] = centers[0][index]
    base_center[1] = centers[1][index]
    return base_center, another

def check_contours(x_range, y_range, contours, previous_center, counter): #y_range and x_range are the max distance the points can be from each other on respective axis
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

    if len(good_centers[0]) >= 2:
        counter += 1
        return [good_centers[0][1]], [good_centers[1][1]], counter
        
    elif len(good_centers[0]) == 0 or len(good_centers[1]) == 0:
        return 0, 0, counter
    else:
        return good_centers[0], good_centers[1], counter


def get_video_centers(video: str): #plays the video and returns centers and the capture object
    global frame_list
    frame_list = []
    cap_centers = [[],[]]
    
    cap = cv2.VideoCapture(video) #sys.argv[1]

    counter = 0
    frames = 0
    another = 0

    while (cap.isOpened()):
        ret, frame = cap.read()
        
        if ret == True:
            frame2 = frame
            frame_list.append(frame2)

            blurred_image = cv2.GaussianBlur(frame, (7,7), 0)
            # read and blur the image
            
            canny = cv2.Canny(blurred_image, 70, 320) #70, 420
            #                                 ^    ^
            #                 change these    |    |  to change contour finding
            contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) == 0:
                continue

            if frames == 0 or another == 1:
                cv2.drawContours(frame, contours, -1 ,(0,255,0), 2)
                base_center, another = get_first_contour(frame, contours, another)

            if another == 0:
                x_c, y_c, counter = check_contours(30, 20, contours, base_center, counter)
                base_center = [x_c, y_c]

                if x_c != 0 or y_c != 0: 
                    cap_centers[0].append(x_c)
                    cap_centers[1].append(y_c)

            scale_percent = 40 # percent of original size
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

vid_centers, capture, num_exc = get_video_centers(sys.argv[1])
print(f"There were {num_exc} times when two points were found in the constraints for the next point")

def sequence_find(x, points):
    RotationCenters = [[], []]
    
    for i in range(0, len(points[0]) - (2 * x), x):
        x1_1 = points[0][i][0]
        y1_1 = points[1][i][0]
        x1_2 = points[0][i+x][0]
        y1_2 = points[1][i+x][0]

        x2_1 = points[0][i+x][0]
        y2_1 = points[1][i+x][0]
        x2_2 = points[0][i+(2*x)][0]
        y2_2 = points[1][i+(2*x)][0]

        line_1 = Line(coor1 = [x1_1, y1_1], coor2 = [x1_2, y1_2])
        line_2 = Line(coor1 = [x2_1, y2_1], coor2 = [x2_2, y2_2])

        line_1.get_m_b()
        line_2.get_m_b()

        if line_1.m == 0 or line_2.m == 0:
            continue

        L1_bisector = get_perpendicular_bisector(line_1)
        L2_bisector = get_perpendicular_bisector(line_2)

        try:
            cor = get_intersection(L1_bisector, L2_bisector)
        except: continue

        RotationCenters[0].append(cor[0])
        RotationCenters[1].append(cor[1])
    return RotationCenters

Cents_Rot = sequence_find(int((len(vid_centers[0])/7)), vid_centers) # first arg is the increment, set here by size of vid_centers / 7 
#                                                                       so it is relative for different sizes of vid_centers
def find_ave_COR(used_cors = [[0,1],[0,1]]):
    for i in range(int(sys.argv[2])):
        x_ave_cor = np.mean(used_cors[0])
        try:
            SD_x_cor = stc.stdev(used_cors[0], xbar = x_ave_cor)
        except:
            continue
        SD_upp_thresh_x = (x_ave_cor + SD_x_cor)
        SD_low_thresh_x = (x_ave_cor - SD_x_cor)

        y_ave_cor = np.mean(used_cors[1])
        try:
            SD_y_cor = stc.stdev(used_cors[1], xbar = y_ave_cor)
        except:
            continue
        SD_upp_thresh_y = (y_ave_cor + SD_y_cor)
        SD_low_thresh_y = (y_ave_cor - SD_y_cor)

        for i in used_cors[0]:
            if i < SD_low_thresh_x or i > SD_upp_thresh_x:
                index1 = used_cors[0].index(i)
                used_cors[0].remove(i)
                used_cors[1].pop(index1)
                #del used_cors[1][index1]

        for j in used_cors[1]:
            if j < SD_low_thresh_y or j > SD_upp_thresh_y:
                index2 = used_cors[1].index(j)
                used_cors[1].remove(j)
                used_cors[0].pop(index2)
                #del used_cors[0][index2]

    ave_x = np.mean(used_cors[0])
    ave_y = np.mean(used_cors[1])
    return used_cors, ave_x, ave_y

Cors_used, ave_cor_x, ave_cor_y = find_ave_COR(Cents_Rot)

print(f"Center of rotation: ({ave_cor_x}, {ave_cor_y}")

plt.figure(figsize = (8,8))

pic = frame_list[int(len(frame_list)/2)]
plt.imshow(pic)

plt.scatter(ave_cor_x, ave_cor_y, color="red", marker='o', zorder=6, label="Average COR") # plots average center of rotation
plt.scatter(Cors_used[0], Cors_used[1], color="green", marker='*', zorder=5, label="COR's after outlier removal")
plt.plot(vid_centers[0], vid_centers[1], color="blue", marker=".", zorder=2, label='Head Movement')

plt.legend(loc="upper right")

cv2.destroyAllWindows()

file_name = sys.argv[1]
file_names = file_name.split("/")
name = file_names[-1].replace(".mp4","")

plt.savefig(f"Plots/{name}.png")

cv2.imwrite(f"PicOutputs/{name}_image.jpg", pic)
plt.show()
file = open(f"TextOutputs/{name}_output.txt", "w")

file.write(f"{str(ave_cor_x)} {str(ave_cor_y)}")

file.close()