import cv2
from final_function import BotFinder
import time
import numpy as np
import threading 
from grid_maker import GridMaker
from video2 import vdo_tbar
import math
from collections import deque
import json
import datetime
import matplotlib.pyplot as plt

global frame
global cX,cY
global point_list


def size_mod(img,times):
    h,w = img.shape[:2]
    dim = (int(w*times), int(h*times))
    return cv2.resize(img, dim)

def click_event(event, x, y, flags, params):

    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # print(params[0])
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y, "pressed left button")   
        # point_list += (x,y,0)
    elif event == cv2.EVENT_RBUTTONDOWN:
        print(x, ' ', y,"pressed right button")   
        # point_list += (x,y,1)

def min_dist(coord_1,coord_2):
    dist = math.sqrt(  (coord_1[0] - coord_2[0])**2  + (coord_1[1] - coord_2[1])**2  )
    return dist

def check_threshold(threshold, dist):
    if dist < threshold:
        True
    else:
        False

def show_line_to_goal(rbt_position, goal):
        cv2.line(frame, rbt_position, goal, color = (255,0,255),thickness = 2 )

def show_trajectory(id):
    global points1
    global points2
    global points3
    global points4
    
    if id  == 1:    
        start_trajectory = points1[0]
        temp_trajectory = deque(list(points1.copy()))
    
    if id  == 2:    
        start_trajectory = points2[0]
        temp_trajectory = deque(list(points2.copy()))

    if id  == 3:    
        start_trajectory = points3[0]
        temp_trajectory = deque(list(points3.copy()))

    if id  == 4:    
        start_trajectory = points4[0]
        temp_trajectory = deque(list(points4.copy()))

    previous_point = temp_trajectory.popleft()
    cv2.circle(frame, (previous_point[0],previous_point[1]), 5, (255,0,255),thickness=-1)
    for point in temp_trajectory:
        cv2.circle(frame, (point[0],point[1]), 5, (255,0,100),thickness=-1)
        cv2.line(frame, previous_point, point, color = (255,255,0),thickness = 2 )
        previous_point = point

def update_points(rbt_position,id):
    global points1
    global points2
    global points3
    global points4
    
    
    # print("in update points")
    threshold = 40

    

    if id == 1:
        dist = min_dist(rbt_position, points1[0])
        # print("the distance found is:", dist, "threshold is:", threshold)
        if threshold > dist:
            if len(points1) > 0:
                points1.popleft()
                # print("popping elements")
            else:pass
                # print("trajectory completed")
    
    if id == 2:
        dist = min_dist(rbt_position, points2[0])
        # print("the distance found is:", dist, "threshold is:", threshold)
        if threshold > dist:
            if len(points2) > 0:
                points2.popleft()
                # print("popping elements")
            else:pass
                # print("trajectory completed")
    if id == 3:
        dist = min_dist(rbt_position, points3[0])
        # print("the distance found is:", dist, "threshold is:", threshold)
        if threshold > dist:
            if len(points3) > 0:
                points3.popleft()
                # print("popping elements")
            else:pass
                # print("trajectory completed")
    if id == 4:
        dist = min_dist(rbt_position, points4[0])
        # print("the distance found is:", dist, "threshold is:", threshold)
        if threshold > dist:
            if len(points4) > 0:
                points4.popleft()
                # print("popping elements")
            else:pass
                # print("trajectory completed")


cap = cv2.VideoCapture('error_imgs/v6.mp4')
ret,frame = cap.read()
# cv2.imshow('frame',frame)
# cv2.setMouseCallback('frame', click_event)


#region video writer ##
# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))

# frame_width_small = int(frame_width/2)
# frame_height_small = int(frame_height/2)

# size = (frame_width, frame_height)
# size_small = (frame_width_small, frame_height_small)
# result = cv2.VideoWriter('error_imgs/big.avi', 
#                          cv2.VideoWriter_fourcc(*'MJPG'),
#                          fps = 30, frameSize = size)
# result_small = cv2.VideoWriter('error_imgs/small.avi', 
#                          cv2.VideoWriter_fourcc(*'MJPG'),
#                          fps = 30, frameSize = size_small)
#endregion

#region point1
points1 = deque([
[1010  , 310],
[1005  , 524],
[1005  , 636],
[998  , 743],
[1140  , 726],
[1281  , 732],
[1426  , 733],
[1492  , 720],
[1342  , 784],
[1136  , 791],
[1004  , 793],
[1007  , 599],
[1003  , 402],
[1005  , 239],
[1007  , 143]])
#endregion

#region point2

points2 = deque([
[937  , 232 ],
[934  , 320 ],
[941  , 391 ],
[934  , 458 ],
[934  , 526 ],
[932  , 593 ],
[935  , 657 ],
[928  , 739 ],
[929  , 806 ],
[1001  , 795 ],
[1066  , 794 ],
[1139  , 795 ],
[1216  , 792 ],
[1284  , 793 ],
[1348  , 790 ],
[1417  , 785 ],
[1488  , 787 ],
[1488  , 787 ],
[1488  , 787 ],
[1389  , 760 ],
[1293  , 778 ],
[1281  , 797 ],
[1212  , 795 ],
[1139  , 792 ],
[1071  , 795 ],
[1004  , 797 ],
[928  , 797 ],
[931  , 728 ],
[926  , 658 ],
[925  , 588 ],
[928  , 524 ],
[932  , 450 ],
[929  , 374 ],
[932  , 303 ],
[931  , 227 ],
[938  , 149 ]
])
#endregion

#region points3

points3 = deque([
[859,   228 ],
[856,   311 ],
[859,   387 ],
[860,   456 ],
[868,   526 ],
[870,   601 ],
[866,   667 ],
[867,   799 ],
[798,   793 ],
[723,   799 ],
[656,   802 ],
[582,   802 ],
[510,   808 ],
[430,   810 ],
[357,   811 ],
[286,   811 ],
[435,   744 ],####
[507,   745 ],
[586,   746 ],
[658,   753 ],
[724,   740 ],
[801,   733 ],
[864,   731 ],
[863,   656 ],
[860,   589 ],
[864,   511 ],
[864,   444 ],
[864,   444 ],
[866,   365 ],
[858,   303 ],
[858,   233 ],
[860,   149 ]])
#endregion

#region point_4
points4 = deque([
[783   ,228 ],
[792   ,307 ],
[797   ,383 ],
[792   ,451 ],
[801   ,528 ],
[800   ,594 ],
[804   ,658 ],
[803   ,731 ],
[722   ,744 ],
[649   ,743 ],
[581   ,743 ],
[509   ,744 ],
[425   ,742 ],
[355   ,748 ],
[282   ,746 ],
[432   ,810 ],
[513   ,806 ],
[585   ,802 ],
[652   ,798 ],
[723   ,798 ],
[792   ,797 ],
[791   ,731 ],
[785   ,655 ],
[788   ,595 ],
[784   ,523 ],
[791   ,449 ],
[786   ,375 ],
[788   ,304 ],
[788   ,224 ],
[786   ,154 ]])
#endregion

#region frame_no
f_no = 0

f_no_1  = 2900
f_no_2 = 6000

f_no_3 = 9200
#endregion

cap.set(cv2.CAP_PROP_POS_FRAMES,0)
s=time.time()

present_time = 0
time_increment = 1/30

while True:
    present_time += time_increment
    time_string = str(datetime.timedelta(seconds = int(present_time)))
    ret,frame = cap.read()
    f_no +=1

    # print(f_no_2)
    # index = cap.get(cv2.CAP_PROP_POS_FRAMES)
    # print("present frame is:", index)
    if ret is False:
        break
    s = time.time()
    BF = BotFinder(frame,f_no)
    bot,f_no = BF.ret()
    for i in bot.keys():
        # info extracted
        cY,cX,angle = bot[i]

        #drawing
        cv2.putText(frame, str(i), (int(cX-10), int(cY)),
        	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.circle(frame, (int(cX),int(cY)), 40, (255,0,255),thickness=2)

        
        # for point in points:
        #     cv2.circle(frame, (point[0],point[1]), 5, (255,0,255),thickness=-1)
        
        # if str(i) == '2210':
            # print(f'angle || {angle}')
        rad = angle*math.pi/180
        radius = 75
        dy = radius*math.sin(rad)
        dx = radius*math.cos(rad)       
        Y = int(cY - dy)
        X = int(cX + dx)
        cv2.line(frame,(int(cX),int(cY)),(X,Y),(0,0,255),2)

    # region ID 2210 ## 
    # if f_no < 2900:
    #     try:
    #         bot_position = (int(bot['2210'][1]), int(bot['2210'][0]))
    #         #print("in the try block")
    #         #print(bot_position)
    #         update_points(bot_position,1)
    #         #print('update_bot_position')
    #         show_line_to_goal(bot_position, points1[0])
    #         #print('line_togoal')
    #         show_trajectory(1)
    #         #print('show_traj')
    #     except:pass
    #         #print(bot)
    #         #print("try block failed")

    # endregion

    #region ID 0122 ##
    # if f_no >2900 and f_no < 6000:
    #     try:
    #         bot_position = (int(bot['0122'][1]), int(bot['0122'][0]))
    #         # print("in the try block")
    #         # print(bot_position)
    #         update_points(bot_position,2)
    #         # print('update_bot_position')
    #         show_line_to_goal(bot_position, points2[0])
    #         # print('line_togoal')
    #         show_trajectory(2)
    #         # print('show_traj')
    #     except:pass
    #         # print(bot)
    #         # print("try block failed")

    #endregion

    #region ID 2010 ##
    # if f_no > 6000 and f_no < 9200:
    #     try:
    #         bot_position = (int(bot['2010'][1]), int(bot['2010'][0]))
    #         # print("in the try block")
    #         # print(bot_position)
    #         update_points(bot_position,3)
    #         # print('update_bot_position')
    #         show_line_to_goal(bot_position, points3[0])
    #         # print('line_togoal')
    #         show_trajectory(3)
    #         # print('show_traj')
    #     except:pass
    #         # print(bot)
    #         # print("try block failed")

    #endregion

    #region ID 2122 ##
    # if f_no > 9200:
    #     try:
    #         bot_position = (int(bot['2122'][1]), int(bot['2122'][0]))
    #         # print("in the try block")
    #         # print(bot_position)
    #         update_points(bot_position,4)
    #         # print('update_bot_position')
    #         show_line_to_goal(bot_position, points4[0])
    #         # print('line_togoal')
    #         show_trajectory(4)
    #         # print('show_traj')
    #     except:pass
    #         # print(bot)
    #         # print("try block failed")

    #endregion
  
    # cv2.putText(frame, time_string, (100, 100),
    #     	cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 3)

    small_frame = size_mod(frame, 0.5)   
    # cv2.imshow('frame',size_mod(frame,0.5))

#region save frames
    # result.write(frame)
    # result_small.write(small_frame)
#endregion
    key = cv2.waitKey(1)
    e = time.time()
    # print(e-s)
    print(f_no)
    if key == 27:
        break
    
#region working with image
# img = [0]
# for i in range(1,38,1):
#     img.append(cv2.imread(f'C:/Users/OHM/Desktop/pytthon/error_imgs/{i}.jpg'))
# feed = cv2.imread(f'C:/Users/OHM/Desktop/pytthon/error_imgs/{63}.jpg')
# # 234567 -->imgs of interest
# for i in range(37,38,1):
#     print(f'in image{i}')
#     s = time.time()
#     # fil = img[i]
#     fil = feed
#     fil_show = size_mod(fil,0.5)
#     cv2.imshow('file', fil_show)    
#     cv2.waitKey()


#     BF = BotFinder(fil)
#     bot= BF.ret()
#     for i in bot.keys():
#         cY,cX,angle = bot[i]
#         cv2.putText(fil, str(i), (int(cX-10), int(cY)),
#        	    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
#         rad = angle*math.pi/180
#         radius = 50
#         dy = radius*math.sin(rad)
#         dx = radius*math.cos(rad)       
#         if angle<0:
#            Y = int(cY - dy)
#         else:
#             Y = int(cY + dy)
#         X = int(cX + dx)
#         cv2.line(fil,(int(cX),int(cY)),(X,Y),(0,0,255),2)

#     print(bot)
#     e = time.time()
#     print(f'time taken = {e-s}')
#     fil_show = size_mod(fil,0.5)
#     cv2.imshow('file', fil)
#     cv2.waitKey()
#     cv2.destroyAllWindows()
#endregion    



