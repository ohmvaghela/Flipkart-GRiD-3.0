import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from video2 import vdo_tbar

from skimage.transform import (hough_line,hough_line_peaks) 
def nothing(x):
    pass


class Angle:
    def __init__(self,img):
        self.ret_degree = 0
        self.img = img

        H,W = self.img.shape[:2]
        copy_img = self.img.copy()

        rgb = cv2.cvtColor(copy_img, cv2.COLOR_BGR2RGB)
        hsv = cv2.cvtColor(copy_img, cv2.COLOR_BGR2HSV)
        # cv2.imshow('rgb', rgb)
        # cv2.imshow('hsv', hsv)
        mask = cv2.inRange(hsv, (0, 0, 220), (255, 100,255))
        # cv2.imshow('img', self.img)
        # cv2.imshow('mask_angle', mask)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        (cnts, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        try:
            c = max(cnts, key = cv2.contourArea)
            x,y,w,h = cv2.boundingRect(c)
            location = [int(y+ h/2), int(x+ w/2)]
            zeros = np.zeros_like(self.img)
            self.angle_b([H,W],location)
            copy_img = cv2.line(copy_img, (int(W/2),int(H/2)), 
                (location[1],location[0]), (255,0,0))
            # cv2.imshow('copy_img', copy_img)
            # cv2.waitKey()

        except:
#            print("failed in angle detection")
            self.ret_degree = 90
            pass
        
#        cv2.line(mask,(location[1],location[0]),(int(W/2),int(H/2)),(255,0,0),1)
#        cv2.line(mask,(int(W/2),0),(int(W/2),int(H)),(255,255,0),2)
#        cv2.line(mask,(0,int(H/2)),(int(W),int(H/2)),(255,255,0),2)


        # cv2.imshow('input_angle', self.img)
        # cv2.imshow('rgb_gray', gray_rgb)
        # cv2.imshow('bgr_gray', gray_bgr)
        
        # cv2.imshow('hls', hsv)
        # cv2.imshow('rgb', rgb)
        # cv2.imshow('mask',mask)

        #plt.imshow(hls)
        #plt.show()        
        #vdo_tbar(copy_img)
        
#        cv2.waitKey()        

    def angle_b(self,img_size,position):
        self.img_size = img_size
        self.position = position
        H,W = self.img_size
        h,w = self.position
        x = w - (W/2)
        y = (H/2) - h
        rad = math.atan2(y , x)
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
        # print(f'initial_angle :: {self.ret_degree}')

    def ret(self):

        (h, w) = self.img.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        # rotate our self.img by 45 degrees around the center of the self.img
        # print(self.ret_degree)
        M = cv2.getRotationMatrix2D((cX, cY), int(90-self.ret_degree), 1.0)
        rotated = cv2.warpAffine(self.img, M, (w, h))

        #croping image
        hsv = cv2.cvtColor(rotated, cv2.COLOR_BGR2HSV)
        pruple_mask = cv2.inRange(hsv,(130, 100, 80), (180, 255,255))
        kernel = np.ones((9,9),np.uint8)
        dilate = cv2.dilate(pruple_mask, kernel)
        edge = cv2.Canny(dilate, 10,250)
        kernel = np.ones((13,13),np.uint8)
        closed = cv2.morphologyEx(edge, cv2.MORPH_CLOSE, kernel)
        (cnts, _) = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        c = max(cnts,key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c) 
        crop_img = rotated[y:y+h,x:x+w]
        # cv2.imshow("Rotated by 45 Degrees", rotated)
        # print(f'angle: {self.ret_degree}')

        # cv2.imshow('crop', crop_img)
        # cv2.imshow('ppl_mask', pruple_mask)
        # cv2.imshow('edge', edge)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        return self.ret_degree,crop_img