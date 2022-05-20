import cv2 
import time
import imutils
import numpy as np
import argparse
import matplotlib.pyplot as plt
import math
# from new_final_function import BotFinder
from angle_only import BotFinder
img = cv2.imread(f'C:/Users/OHM/Desktop/pytthon/error_imgs/66.jpg')


#region for all functions
# BF = BotFinder()

# BF.give_frame(img)

# bot = BF.ret()
# print(bot)
#endregion

#region just orientation and loaction
BF = BotFinder()
BF.give_frame(img)
angle, location = BF.ret()

cY,cX = location[0]
cv2.circle(img, (int(cX),int(cY)), 40, (255,0,255),thickness=2)

rad = angle*math.pi/180
radius = 75
dy = radius*math.sin(rad)
dx = radius*math.cos(rad)       
Y = int(cY - dy)
X = int(cX + dx)
cv2.line(img,(int(cX),int(cY)),(X,Y),(0,0,255),2)

cv2.imshow('img',img)
cv2.waitKey(0)
#endregion

#region video 
# cap = cv2.VideoCapture('error_imgs/v8.mp4')
# ret,frame = cap.read()

# while True:
#     ret,frame = cap.read()
#     if ret is False:break 
#     BF = BotFinder()
#     BF.give_frame(frame)
#     angle, location = BF.ret()

#     cY,cX = location[0]
#     cv2.circle(frame, (int(cX),int(cY)), 40, (255,0,255),thickness=2)

#     rad = angle*math.pi/180
#     radius = 75
#     dy = radius*math.sin(rad)
#     dx = radius*math.cos(rad)       
#     Y = int(cY - dy)
#     X = int(cX + dx)
#     cv2.line(frame,(int(cX),int(cY)),(X,Y),(0,0,255),2)

#     cv2.imshow('frame',frame)
#     key = cv2.waitKey(1)
#     if key == 27:break
#endregion