##mew
import cv2
from final_function import BotFinder
import time
import numpy as np
import threading 

img = cv2.imread('Resources/arena_high.png')
cam_feed1 = cv2.imread('Resources/cam_feed_1.jpeg')
cam_feed2 = cv2.imread('Resources/cam_feed_2.jpeg')
cam_feed3 = cv2.imread('Resources/cam_feed_3_edit.jpeg')
cam_feed4 = cv2.imread('Resources/photo2.jpg')
vdo_feed = cv2.VideoCapture('Resources/video_M3.mp4')
feed_img = cam_feed4.copy()


no_time = 0
iteratio = 0
while True:
    start = time.time()

    _,frame = vdo_feed.read()
    f2 = frame.copy()
    try:
        BF = BotFinder(f2)
        bot= BF.ret()
        iteratio += 1
        for i in bot.keys():
            cY,cX,_ = bot[i]
            txt2 = f' fail : {no_time} || Iteration : {iteratio}'
            cv2.putText(frame, txt2, (200, 100),
        	    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 2)
            cv2.putText(frame, str(i), (int(cX-10), int(cY)),
        	    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    except:
        no_time+=1
        cv2.imwrite(f'error_imgs/img{no_time}.jpg', f2)


    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key == 27:
        break 
    end = time.time()
    print((1/(end-start)))




#BF = BotFinder(feed_img)
#bot= BF.ret()
#for i in bot.keys():
#    cY,cX,_ = bot[i]
#    cv2.putText(feed_img, str(i), (int(cX-10), int(cY)),
#    	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
#e = time.time()
#cv2.imshow('',feed_img)
#cv2.waitKey()


# print results
# print(f'runtime = {e-s}')

#print(bot)
#cv2.imshow('img', cam_feed1)
#cv2.waitKey()
#print(orientation)
print("location is (height,width) with origin at top left cornor")