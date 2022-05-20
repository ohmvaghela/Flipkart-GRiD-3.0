import cv2
import numpy as np
import math
from skimage.transform import (hough_line,hough_line_peaks) 
def nothing(x):
    pass


class Angle:
    def __init__(self,img):
        self.ret_degree = 0
        self.img = img
        H,W = self.img.shape[:2]
        copy_img = self.img.copy()
        hsv = cv2.cvtColor(copy_img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([40, 50, 50])
        upper_blue = np.array([70, 255, 150])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        #cv2.imshow('s',mask)
        key = cv2.waitKey()
        (cnts, _) = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) 
        c = max(cnts, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        location = [int(y+ h/2), int(x+ w/2)]
        zeros = np.zeros_like(self.img)
        self.angle_b([H,W],location)

#        cv2.line(mask,(location[1],location[0]),(int(W/2),int(H/2)),(255,0,0),1)
#        cv2.line(mask,(int(W/2),0),(int(W/2),int(H)),(255,255,0),2)
#        cv2.line(mask,(0,int(H/2)),(int(W),int(H/2)),(255,255,0),2)
#        cv2.imshow('',mask)
#        cv2.waitKey()        

    def angle_b(self,img_size,position):
        self.img_size = img_size
        self.position = position
        H,W = self.img_size
        h,w = self.position
        x = w - (W/2)
        y = (H/2) - h
        rad = math.atan2(y,x)
        degree = rad*180/math.pi
        # if   y>0 and degree <=0:
        #     Degree = 180 - degree
        # elif y>0 and degree >0:
        #     Degree = degree
        # elif y<=0 and degree >=0:
        #     Degree = degree - 180
        # elif y<=0 and degree <0:
        #     Degree = degree
        self.ret_degree = degree

    def ret(self):
        return self.ret_degree