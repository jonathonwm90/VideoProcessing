# final_vid_process.py VID_EDITED/side_head1.mp4 3

import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
from geometry import *
import statistics as stc
# this is atest of the reload
plt.style.use('_mpl-gallery')

def format_contour(x: int, contours: list):# gets the (x,y) coordinates for the desired contour, and plots it
    formatted_contours = []
    for i in range(len(contours[0])):
        formatted_contours.append(contours[x][i][0])
    
    xvars, yvars = [], []
    for i in range(len(formatted_contours)):
        np.array(formatted_contours)
        xvars.append(formatted_contours[i][0])
        yvars.append(formatted_contours[i][1])
   
    #plt.scatter(xvars, yvars, color="green", marker=".")
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

    #plt.plot(x_ave, y_ave, color="blue", marker="*" )
    return x_ave, y_ave, contour1

def check_contours(x_range, y_range, contours):
    centers = [[],[]]
    x_ext, y_ext = []
    for i in range(len(contours)):
        x_cent, y_cent, contour = get_contour_center(i, contours)
        centers[0].append(x_cent)
        centers[1].append(y_cent)
        x_ext.append([contour[0][0], contour[0][-1]])
        y_ext.append([contour[1][0], contour[1,[-1]]])
    
    for i in range(len(centers[0])):
        if (abs(centers[0][i] - x_ext[i][0])) < (x_range/2) and (abs(centers[0][i] - x_ext[i][1])) < (x_range/2):
            pass
        

        if (abs(centers[1][i] - y_ext[i][0])) < (y_range/2) and (abs(centers[1][i] - y_ext[i][1])) < (y_range/2):
            pass



def get_video_centers(video: str): #plays the video and returns centers and the capture object
    cap_centers = [[],[]]

    cap = cv2.VideoCapture(video) #sys.argv[1]
    frames = 0

    while (cap.isOpened()):
        ret, frame = cap.read()
        try:
            if frames%10 == 0:
                plt.imshow(frame, alpha=.2)
        except:
            pass

        if ret == True:

        # Capture frame-by-frame

            blurred_image = cv2.GaussianBlur(frame, (7,7), 0)
            # read and blur the image

            canny = cv2.Canny(blurred_image, 70, 420) 
            #                                 ^    ^
            #                 change these    |    |  to change contour finding
            contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) == 0 or len(contours) > 1:
                continue
            
            get_contour_center(0, contours, cap_centers)

            cv2.drawContours(frame, contours,  -1, (0,255,0), 2)
            cv2.imshow("objects Found", frame)

            frames += 1

        else:
            break

        if cv2.waitKey(25) == ord('q'): #not sure what this does, but you need it.
            break
    cap.release()
    return cap_centers, cap

vid_centers, capture = get_video_centers(sys.argv[1])

def sequence_find(x, points):
    RotationCenters = [[], []]

    for i in range(0, len(points[0]) - (2 * x), x):
        

        x1_1 = points[0][i]
        y1_1 = points[1][i]
        x1_2 = points[0][i+x]
        y1_2 = points[1][i+x]

        x2_1 = points[0][i+x]
        y2_1 = points[1][i+x]
        x2_2 = points[0][i+(2*x)]
        y2_2 = points[1][i+(2*x)]

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

Cents_Rot = sequence_find(3, vid_centers)

def find_ave_COR(used_cors = [[0,1],[0,1]]):
    for i in range(int(sys.argv[2])):
        
        x_ave_cor = np.mean(used_cors[0])
        SD_x_cor = stc.stdev(used_cors[0], xbar = x_ave_cor)
        SD_upp_thresh_x = (x_ave_cor + SD_x_cor)
        SD_low_thresh_x = (x_ave_cor - SD_x_cor)

        y_ave_cor = np.mean(used_cors[1])
        SD_y_cor = stc.stdev(used_cors[1], xbar = y_ave_cor)
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
print(ave_cor_x, ', ', ave_cor_y)
plt.scatter(ave_cor_x, ave_cor_y, color="red", marker='o', zorder=6, label="Average COR")

#plt.scatter(Original_cors[0], Original_cors[1], color="purple", marker='+', zorder=3, label="COR's before outlier removal")
plt.scatter(Cors_used[0], Cors_used[1], color="green", marker='*', zorder=5, label="COR's after outlier removal")
#plt.scatter(ave_cor_x, ave_cor_y, color="red", marker='o', zorder=6, label="Average COR")
plt.plot(vid_centers[0], vid_centers[1], color="blue", marker=".", zorder=2, label='Head Movement')

plt.legend(loc="upper right")

# release the video capture object

# Closes all the windows currently opened.
cv2.destroyAllWindows()

plt.show()