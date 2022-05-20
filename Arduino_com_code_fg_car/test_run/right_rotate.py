## only for ratating image by pi/2 radians according 
# to green square loaction

import cv2
import numpy as np
import imutils
 

class RotateImage:
    def __init__(self,img):
        self.img = img
        self.cX = 0
        self.cY = 0
        self.ac_rotation = 0
        self.h, self.w = self.img.shape[:2]
        self.total_area = self.h * self.w
        self.total_rotate = 0

    def SqCenter(self):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))

        blurred = cv2.blur(mask, (10, 10))

 #       cv2.imshow('blured', blurred)
 #       cv2.imshow('thresh',mask)
 #       cv2.imshow('gray',hsv)
 #       cv2.waitKey()
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
        	cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        for c in cnts:
#            print(f'cnt area{cv2.contourArea(c)}||total_area {self.total_area}')
            if cv2.contourArea(c) > (0.005*self.total_area):
                M = cv2.moments(c)
        self.cX = int(M["m10"] / M["m00"])
        self.cY = int(M["m01"] / M["m00"])

#        print(f'w:{self.w} | x:{self.cX}')
#        print(f'w:{self.h} | x:{self.cY}')
#        print("right rotate image function")
#        cv2.circle(self.img, (self.cX, self.cY), 5, (255, 255, 255), -1)

        if self.cY < int(self.h/4):
            pass
        elif self.cX > int(self.w * 3 /4) : 
            self.img = cv2.rotate(self.img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.total_rotate = 90
#           print('90 clock active')
        elif self.cY > int(self.h * 3 /4): 
            self.img = cv2.rotate(self.img, cv2.cv2.ROTATE_180)
            self.total_rotate = 180
#            print('180 active')
        elif self.cX < int(self.w /4): 
            self.img = cv2.rotate(self.img, cv2.cv2.ROTATE_90_CLOCKWISE)
            self.total_rotate = 270
#            print('90 ac active')
        
        
#        cv2.imshow('aligned', self.img)
#        cv2.waitKey()
#        cv2.destroyAllWindows()
        return self.img,self.total_rotate
        
