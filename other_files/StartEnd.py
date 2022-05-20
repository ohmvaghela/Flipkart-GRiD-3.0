import cv2
from final_function import BotFinder
import time
import math
import numpy as np
import pandas as pd
import matplotlib.image as mpimg

class Start_End:
    def __init__(self,img):
        self.img = img
        self.hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        self.yellow_down = np.array([30,90,80])
        self.orange_down = np.array([12,90,165])
        self.green_down = np.array([50,90,140])
        self.red_down = np.array([0,90,200])    
        self.yellow_up = np.array([ 50,255,255])
        self.orange_up = np.array([ 23,255,255])
        self.green_up = np.array([ 90,255,255])
        self.red_up = np.array([ 10,255,255])  
        self.number = 0  
        self.lower_lim = 0
        self.upper_lim = 0

    def start_color(self,number):
        pass
        if self.number == 1:
            self.upper_lim = self.yellow_up
            self.lower_lim = self.yellow_down
        elif self.number == 2:
            self.upper_lim = self.orange_up
            self.lower_lim = self.orange_down
        elif self.number == 3:
            self.upper_lim = self.green_up
            self.lower_lim = self.green_down
        elif self.number == 4:
            self.upper_lim = self.red_up
            self.lower_lim = self.red_down
        
    #def start_end_coord(hsv_img,lower_lim,upper_lim):
    def start_end_coord(self,number):
        self.number = number
        self.start_color(self.number)
        mask = cv2.inRange(self.hsv, self.lower_lim, self.upper_lim)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        coord = []
        biggest_cnt = max(contours,key=cv2.contourArea)
        min_area = 0.1*cv2.contourArea(biggest_cnt)
        for c in contours:
            if cv2.contourArea(c) < min_area:
                continue
#            cv2.drawContours(self.hsv, c, -1, (255,255,0),thickness=5)
#            cv2.waitKey()
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
