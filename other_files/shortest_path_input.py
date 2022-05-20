##mew
import cv2
from final_function import BotFinder
import time
import math
import numpy as np
import pandas as pd
import matplotlib.image as mpimg
from StartEnd import Start_End

def size_mod(img,times):
    h,w = img.shape[:2]
    dim = (int(w/times), int(h/times))
    return cv2.resize(img, dim)

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
    # cv2.waitKey(1)

img = []
for i in range(1,27,1):
    # print(i)
    img.append(cv2.imread(f'C:/Users/OHM/Desktop/pytthon/error_imgs/{i}.jpg'))




feed = img[25]
feed = cv2.imread(f'C:/Users/OHM/Desktop/pytthon/error_imgs/26.jpg')


cv2.imshow('frame',feed)
# cv2.waitKey()
SE = Start_End(feed)
coordD = SE.start_end_coord(1)
# print(coordD)




hsv = cv2.cvtColor(feed, cv2.COLOR_BGR2HSV)
lower_blue = np.array([30,90,80])
upper_blue = np.array([50,255,255])
# coord = start_end_coord(hsv,lower_blue ,upper_blue )
# print(f'1 --> start point: {coord[0]} || end point: {coord[1]}')
height,width = feed.shape[:2]

#dim = (int(w/2), int(h/2))
#feed = cv2.resize(feed, dim)
s = time.time()
gray = cv2.cvtColor(feed, cv2.COLOR_BGR2GRAY)
hls = cv2.cvtColor(feed, cv2.COLOR_BGR2HLS)
mask = cv2.inRange(hls, (0,100,0), (255,255,255))
blur = cv2.GaussianBlur(mask, (5,5), 0)
blur = cv2.GaussianBlur(blur, (5,5), 0)
kernel = np.ones((5,5), np.uint8)
thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
kernel = np.ones((13,13), np.uint8)
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
kernel = np.ones((3,3), np.uint8)
img_erosion = cv2.erode(closing, kernel, iterations=1)

# test(mask,'mask')
# test(blur,'blur')
# test(thresh,'thresh')
# test(opening,'img_dilation')
# test(closing,'closing')
# test(img_erosion,'img_erosion')

#img_dilation = cv2.dilate(blur, kernel, iterations=5)
#print("dilated inage")
#
contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
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
    x,y,w,h = cv2.boundingRect(c)
    
    ratio = w/h
    if cnt_area > min_area and cnt_area < max_area and len(approx) == 4 :
        #print(len(approx))
        if ratio > 2 or ratio < 0.5:
            continue 
#     if cnt_area > 2250 and cnt_area < 6300 and len(approx) == 4:
        
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
        # test(size_mod(feed, 2) ,'empty')
        test(feed,'wew')
        # cv2.waitKey(100)
        
cv2.waitKey()

#region matrix initialisation
matrix_x = np.zeros((10,18))
matrix_y = np.zeros((10,18))
value = np.zeros((10,18))
#endregion

#region finding nearest box "left_bottom_key"
left_bottom_location = (0,height)
left_bottom_key = 1
minimum_distace = min_dist(left_bottom_location, boxes[1])
#finding left bottom block
for i in range(1,69,1):
        sepreation = min_dist(left_bottom_location, boxes[i])
        if sepreation < minimum_distace:
            minimum_distace = sepreation
            left_bottom_key = i
#endregion

#region approx "radius" btwn 2 consecutive blocks 
diameter = min_dist(boxes[1], boxes[i])
for i in range(2,69,1):
    temp_diameter = min_dist(boxes[1], boxes[i])
    if temp_diameter < diameter:
            diameter = temp_diameter
radius = diameter//2
# print(radius)
#endregion

# 2 rows 10 column
keys_in_range = []
for i in range(2):#last and second-last row 
    #going through all boxes 
    for i in range(1,64,1):
        y_current = boxes[left_bottom_key][1]

        


    col = 6
    for j in range(4):
        post = boxes[key]
        matrix_x[row,col] = post[0]
        matrix_y[row,col] = post[1]
        value[row,col] = True
        
        #print(f'{post[0]} : {post[1]} :: {post}')
        #print(f'{matrix_x[row,col]} : {matrix_y[row,col]} :: {post}')

        #print(matrix_x)
        #print(matrix_y)
        col +=1
    key +=1
    row -=1
row = 1
for i in range(2):
    col = 0
    for i in range(16):
        post = boxes[key]
        #print(post)
        matrix_x[row,col] =post[0]
        matrix_y[row,col] = post[1]
        value[row,col] = True
        col +=1
        key +=1
    row -=1
final = list(zip(matrix_x, matrix_y,value))
i=0
a = final.copy()
for i in range(len(matrix_x)):
    final[i] = list(zip(matrix_x[i], matrix_y[i],value[i]))
df = pd.DataFrame(final)

block_sepearation = min_dist(df[0][0], df[0][1])

#print(df)
# print(len(df),len(df[1]),len(df[0]))
# print(f'{df[0][0]} : {df[0][1]} --> {block_sepearation}')
# e = time.time()
# print(e-s)

# bot_position is (x,y)
bot_position = [700,700]
min_sep = block_sepearation*0.1
bot_x = bot_position[0]
bot_y = bot_position[1]

