# final_vid_process.py VID_EDITED/side_head1.mp4 3

import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
from geometry import *
import statistics as stc

plt.style.use('_mpl-gallery')

def format_contour(x: int, contours: list):# gets the (x,y) coordinates for the desired contour, and plots it
    
    formatted_contours = []
    for i in range(len(contours[x][0])):
        
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

def check_contours(x_range, y_range, contours, previous_center): #y_range and x_range are the max distance the points can be from each other on respective axis
    centers = [[],[]]
    good_centers = [[],[]]
    contours_f = [[],[]]
    for i in range(len(contours)):
        x_cent, y_cent, contour = get_contour_center(i, contours)
        contours_f[0].append(contour[0])
        contours_f[1].append(contour[1])
        centers[0].append(x_cent)
        centers[1].append(y_cent)
        
    for i in range(len(centers[0])):
        if (abs(centers[0][i] - previous_center[0])) < (x_range) and (abs(centers[1][i] - previous_center[1])) < (y_range):
            good_centers[0].append(centers[0][i])
            good_centers[1].append(centers[1][i])

    if len(good_centers[0]) >= 2:
        plt.plot(good_centers[0], good_centers[1], color="pink", marker="*")
        plt.scatter(contours_f[0], contours_f[1], color="green", marker=".")
        plt.imshow(start_frame)
        plt.show()
        print(good_centers)
        raise Exception("two points were found in the constraints for the next point")
    elif len(good_centers[0]) == 0 or len(good_centers[1]) == 0:
        return 0, 0
    else:
        return good_centers[0][0], good_centers[1][0]


def get_video_centers(video: str): #plays the video and returns centers and the capture object
    cap_centers = [[],[]]
    bad_centers = [[],[]]

    cap = cv2.VideoCapture(video) #sys.argv[1]
    frames = 0
    another = 0

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
            
            canny = cv2.Canny(blurred_image, 70, 275) #70, 420
            #                                 ^    ^
            #                 change these    |    |  to change contour finding
            contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            #if len(contours) == 0 or len(contours) > 1:
            #    continue
            if len(contours) == 0:
                continue
            if frames == 0 or another == 1:
                old_x = 0
                old_y = 0

                global start_frame
                start_frame = frame

                counter = 1

                for i in contours:
                    x, y, thing = get_contour_center(0, [i], bad_centers)
                    print(counter, len(contours))
                    if counter == len(contours):
                        print("success")
                        another = 1
                        continue

                    if abs(old_x - x) < 30:
                        continue
                    
                    if abs(old_y - y) < 30:
                        continue
                    cv2.drawContours(blurred_image, contours, -1 ,(0,255,0), 2)
                    cv2.imshow("objects Found", blurred_image)
                    plt.imshow(frame)
                    plt.plot(x, y, color="purple", marker=".")
                    plt.show()
                    answr = input("Is that the right center, y or n: ")
                    
                    old_x = x
                    old_y = y
                    counter += 1

                    if answr == 'y':
                        base_center = [x,y]
                        another = 0
                        break
                    else:
                        continue
                    
            if another == 0:
                x_c, y_c = check_contours(50, 40, contours, base_center)

                if x_c != 0 or y_c != 0: 
                    cap_centers[0].append(x_c)
                    cap_centers[1].append(y_c)

            #get_contour_center(0, contours, cap_centers)
            cv2.drawContours(frame, contours, -1 ,(0,255,0), 2)
            cv2.imshow("objects Found", frame)

            frames += 1

        else:
            break

        if cv2.waitKey(25) == ord('q'): #not sure what this does, but you need it.
            break
    cap.release()
    return cap_centers, cap

vid_centers, capture = get_video_centers(sys.argv[1])
print(vid_centers)
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

        #print(line_1.y1, line_1.m, line_1.x1)

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
print(Cents_Rot)

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