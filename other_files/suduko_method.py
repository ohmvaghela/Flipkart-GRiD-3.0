##mew
import cv2
from final_function import BotFinder
import time
import math
import numpy as np
import pandas as pd
import matplotlib.image as mpimg
from StartEnd import Start_End


def draw_cnts(img):    
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    area = img.shape[:2][1]*img.shape[:2][0]
    min_area = area*(0.0009)
    max_area = area*(0.01)
    i = 0
    boxes = {}
    coord = []
    for c in contours:

        cnt_area = cv2.contourArea(c)
        #if cnt_area > min_area/5 and cnt_area < 10* min_area:
        peri = cv2.arcLength(c, True)
        #approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        approx = cv2.approxPolyDP(c, 0.03 * peri, True)
        #if True:
        if cnt_area > min_area and cnt_area < max_area and len(approx) == 4:
            print(len(approx))
    #     if cnt_area > 2250 and cnt_area < 6300 and len(approx) == 4:
            i +=1
            #cv2.drawContours(feed, c, -1, (0,255,0),thickness=5)
            #print(f'{area} || {min_area} || {cnt_area} ')
            #print(f'{i} : area= {area} : {cnt_area} : len: {len(approx)}')
            try:
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                center_location = (cX,cY)
                boxes[i] = center_location
                coord.append(center_location)
                # draw the contour and center of the shape on the image
                cv2.drawContours(img, [c], -1, (0, 255, 0), 5)
                cv2.circle(img, (cX, cY), 30, (255, 255, 0), 4)
                cv2.circle(img, (cX, cY), 4, (255, 0, 255), -1)
                cv2.putText(img, str(i), (cX - 10, cY - 10),
            	cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
            except :
                pass
    test(img,'empty')



def start_end_coord(hsv_img,lower_lim,upper_lim):
#def start_end_coord(self,hsv_img,lower_lim,upper_lim):
    #1_yellow = 30,90,80: 50,255,255
    #2_orange = 12,90,165: 23,255,255
    #3_green = 50,90,140: 90,255,255
    #4_red = 0,90,200: 10,255,255    
    mask = cv2.inRange(hsv_img, lower_lim, upper_lim)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    coord = []
    biggest_cnt = max(contours,key=cv2.contourArea)
    min_area = 0.1*cv2.contourArea(biggest_cnt)
    for c in contours:
        if cv2.contourArea(c) < min_area:
            continue
        cv2.drawContours(hsv_img, c, -1, (255,255,0),thickness=5)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            # set values as what you need in the situation
            cX, cY = 0, 0
        coord.append((cX,cY))
    if coord[0][1] < coord[1][1]:
        coord[0],coord[1] = coord[1],coord[0]
    return coord# coord[0] is start (_,_) and corrd[1] is end

def min_dist(coord_1,coord_2):
    dist = math.sqrt(  (coord_1[0] - coord_2[0])**2  + (coord_1[1] - coord_2[1])**2  )
    return dist

def test(img,name):
    name = str(name)
    cv2.imshow(name,img)
    cv2.waitKey()

def size_mod(img,times):
    h,w = img.shape[:2]
    dim = (int(w/times), int(h/times))
    return cv2.resize(img, dim)

img = []
for i in range(1,12,1):
    img.append(cv2.imread(f'C:/Users/OHM/Desktop/pytthon/error_imgs/{i}.jpg'))

# 234567 -->imgs of interest
fil = img[8]

fil = size_mod(fil, 1)


feed = fil.copy()
kernel = np.ones((3,3),np.uint8)
gradient = cv2.morphologyEx(feed, cv2.MORPH_GRADIENT, kernel)
#cv2.imshow('1gradient',gradient)

gray = cv2.cvtColor(gradient,cv2.COLOR_BGR2GRAY)
#cv2.imshow('2gray', gray)

#_,thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
#cv2.imshow('thresh', thresh)

blur = cv2.GaussianBlur(gray, (7,7), 0)
# cv2.imshow('3blur', blur)
kernel = np.ones((3,3),np.uint8)
dilate = cv2.morphologyEx(blur, cv2.MORPH_ERODE, kernel)
# cv2.imshow('4dialte', dilate)
kernel = np.ones((7,7),np.uint8)
close_1 = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
cv2.imshow('5close1',close_1)
kernel = np.ones((5,5),np.uint8)
#dilate = cv2.morphologyEx(close_1, cv2.MORPH_ERODE, kernel)

h,w = close_1.shape[:2]
top = close_1[0:int(h/2),:]
bottom = close_1[int(h/2):h,:]
_,thresh_top = cv2.threshold(top, 20, 255, cv2.THRESH_BINARY)
_,thresh_bottom = cv2.threshold(bottom, 50, 255, cv2.THRESH_BINARY)
thresh = np.zeros_like(close_1)
thresh[0:int(h/2),:] = thresh_top
thresh[int(h/2):h,:] = thresh_bottom
kernel = np.ones((13,13),np.uint8)
close_1 = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
cv2.imshow('close_1', close_1)
cv2.waitKey()





contours, _ = cv2.findContours(close_1, 
    cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
area = feed.shape[:2][1]*feed.shape[:2][0]
#min_area = area*(0.0019)
#max_area = area*(0.0048)
min_area = area*(0.0009)
max_area = area*(0.01)

#print(f'{min_area}::{max_area} ')
i = 0
boxes = {}
coord = []
for c in contours:
    
    cnt_area = cv2.contourArea(c)
    #if cnt_area > min_area/5 and cnt_area < 10* min_area:
    peri = cv2.arcLength(c, True)
    #approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    approx = cv2.approxPolyDP(c, 0.03 * peri, True)
    if cnt_area > min_area and cnt_area < max_area:# and len(approx) == 4:
#     if cnt_area > 2250 and cnt_area < 6300 and len(approx) == 4:
        x,y,w,h = cv2.boundingRect(c)
        length = 2*math.sqrt(cnt_area)
        if w > length or h> length:
            continue
        i +=1
        #cv2.drawContours(feed, c, -1, (0,255,0),thickness=5)
        #print(f'{area} || {min_area} || {cnt_area} ')
        #print(f'{i} : area= {area} : {cnt_area} : len: {len(approx)}')
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        center_location = (cX,cY)
        boxes[i] = center_location
        coord.append(center_location)
        # draw the contour and center of the shape on the image
        cv2.drawContours(feed, [c], -1, (0, 255, 0), 2)
        cv2.circle(feed, (cX, cY), 30, (255, 255, 0), 4)
        cv2.circle(feed, (cX, cY), 4, (255, 0, 255), -1)
        cv2.putText(feed, str(i), (cX - 10, cY - 10),
    	cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
print(i)
test(feed,'empty')
