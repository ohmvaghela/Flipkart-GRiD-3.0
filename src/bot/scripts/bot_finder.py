#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from base_class import BotFinder,img_align,orientation_line_from_angle,size_mod
import cv2 
import time
import imutils
import numpy as np
import argparse
import matplotlib.pyplot as plt
from skimage.transform import (hough_line,hough_line_peaks) 
import math
from std_msgs.msg import Float32MultiArray


def callback(data):
    rospy.loginfo("Received message: %s", data.data)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('chatter', String, callback)
    rospy.spin()


if __name__ == '__main__':
  # initialiser
    output_publisher = rospy.Publisher('output_array_topic', Float32MultiArray, queue_size=10)
    output_array_msg = Float32MultiArray()

    BF = BotFinder() # BotFinder()
    pts = [[570,150],[1340,190],[1360,990],[500,970]] # img24.jpg
    pts_plus = [[520,95],[1390,140],[1420,1050],[440,1030]] # img24 with startpts

    # video capture

    vdo = cv2.VideoCapture('C:/Users/OHM/Desktop/pytthon/Resources/image/test1/vdo2.mp4')
    # vdo = cv2.VideoCapture(2)
    # vdo.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # vdo.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


    ret,img = vdo.read()    
    img_aligned_plus= img_align(img,pts_plus,1600,1600)  
    # print(img.shape[:2])
    # cv2.imshow('img1',img)          
    # cv2.imshow('img',img_aligned_plus)
    cv2.waitKey()

    ret,saved_img = vdo.read()
    filename = 'abcd.jpg'

    while True:
        start = time.time()
        ret,img = vdo.read()
        if ret is False:break 
        
        # img_aligned= img_align(img,pts,1400,1400)
        img_aligned_plus= img_align(img,pts_plus,1600,1600)            
        img_copy = img_aligned_plus.copy()
        # cv2.imshow("plot_img",size_mod(img_copy,0.5))

        # cv2.imshow("plot_img",img_copy)
        
        BF.give_frame(img_aligned_plus)
        bot = BF.ret()
        output_array_msg.data = bot
        output_publisher.publish(output_array_msg)

        for i in bot.keys():
            # extract info from bot
            cY,cX,angle = bot[i]
            # print(bot)
            #draw circle and show bot ID  
            cv2.putText(img_copy, str(i), (int(cX-10), int(cY)),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
            cv2.circle(img_copy, (int(cX),int(cY)), 30, (0,255,255),thickness = 2)

            # draw line of orientation
            orientation_line_from_angle(img_copy, angle, (cX,cY))
        
        cv2.imshow("plot_img",size_mod(img_copy,0.5))
        key = cv2.waitKey(20)
        if key == 27:break
        end = time.time()    