import cv2
from final_function import BotFinder
import time
import numpy as np

#cam_feed1 = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/cam_feed_1.jpeg')
#cam_feed2 = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/cam_feed_2.jpeg')
#cam_feed3 = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/cam_feed_3.jpeg')
#img = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/arena_high.png')

# image loaction
img = cv2.imread('Resources/arena_high.png')
cam_feed1 = cv2.imread('Resources/cam_feed_1.jpeg')
cam_feed2 = cv2.imread(r"D:\Robotics\FlipkartD2C\grid 3.0\ohm_scripts\bot_det\cam_feed1.jpeg")
cam_feed3 = cv2.imread('Resources/cam_feed_3_edit.jpeg')
#cam_feed3 = cv2.imread('Resources/cam_feed_1.jpeg')
#image to be feed 
feed_img = cam_feed2.copy()


# load image
#cv2.imshow('winname', feed_img)
#cv2.waitKey()
#cv2.destroyAllWindows()


# bot location and ID 
# s = time.time()
BF = BotFinder(feed_img)
bot= BF.ret()
for i in bot.keys():
    cY,cX,_ = bot[i]
    cv2.putText(cam_feed3, str(i), (int(cX-10), int(cY)),
    	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
e = time.time()
# cv2.imshow('',cam_feed3)
# cv2.waitKey()
# print results
# print(f'runtime = {e-s}')
print(bot)
#cv2.imshow('img', cam_feed1)
#cv2.waitKey()
#print(orientation)
print("location is (height,width) with origin at top left cornor")