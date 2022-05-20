# original lib
import cv2 
import time
import imutils
import numpy as np
import argparse

# my lib
from align_tester import Alignimage
from contour_finder import C_T_iden_fn
from extract_contours import ExtractContour
from grid_maker import GridMaker
from right_rotate import RotateImage
from shape_det import ShapeDetector
from angle import Angle


class BotFinder:
    def __init__(self,img,f_no):
        
        self.img = img
        self.f_no = f_no
        self.BotID = []
        self.bot_angle = []
        self.Bot = {}
        self.AC_orientation = []
        path = 'C:/Users/OHM/Desktop/pytthon/'

        ext = ExtractContour(self.img)
        bot_img,self.bot_location = ext.ret()
        
        #region show extracted bot
        # for i in range(len(bot_img)):
        #    cv2.imshow(f'{i}', bot_img[i])
        # cv2.waitKey()
        #endregion
       
        aligned_images = []
        sd = ShapeDetector()
        
        for i in range(len(bot_img)):
            bot_img[i] = cv2.resize(bot_img[i], (int( bot_img[i].shape[1]*4) , int(bot_img[i].shape[0]*4)))            
#       
            Agl = Angle(bot_img[i])
            degree,rotated_img = Agl.ret()
            self.AC_orientation.append(degree)
            
            ##aligning image manually
            aligned_images = rotated_img
            #region masked bot images  ##
            # if i ==0:
            #     hsv = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2HSV)
            #     mask = cv2.inRange(hsv, (30, 0, 150), (80, 50,255))
            #     cv2.imshow('mask_1', mask)

            # elif i ==1:
            #     hsv = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2HSV)
            #     mask = cv2.inRange(hsv, (30, 0, 150), (80, 50,255))
            #     cv2.imshow('mask_2', mask)

            # elif i ==2:
            #     hsv = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2HSV)
            #     mask = cv2.inRange(hsv, (30, 0, 150), (80, 50,255))
            #     cv2.imshow('mask_3', mask)

            # elif i ==3:
            #     hsv = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2HSV)
            #     mask = cv2.inRange(hsv, (30, 0, 150), (80, 50,255))
            #     cv2.imshow('mask_4', mask)
            #endregion

            gd = GridMaker(rotated_img,self.f_no,i)#,self.f_no)
            bot_id = gd.IdFinder()

            # bot_id,self.f_no = gd.IdFinder()
            # print(f'bot_id : {bot_id}')
            # print(f'bot location: {self.bot_location[i]}')
            
            self.BotID.append(bot_id)                      
            self.Bot[str(bot_id)] = self.bot_location[i]


 
            
            if str(bot_id) == '2210':
                cv2.imwrite(path + f'colored_bot/{str(bot_id)}/{self.f_no}.png', rotated_img)
            if str(bot_id) == '0122':
                cv2.imwrite(path + f'colored_bot/{str(bot_id)}/{self.f_no}.png', rotated_img)
            if str(bot_id) == '2010':
                cv2.imwrite(path + f'colored_bot/{str(bot_id)}/{self.f_no}.png', rotated_img)
            if str(bot_id) == '2122':
                cv2.imwrite(path + f'colored_bot/{str(bot_id)}/{self.f_no}.png',rotated_img)
            
            

    def ret(self):    
        count = 0
        for i in self.Bot.keys():
            temp = self.Bot[i]
            self.Bot[i] = [temp[0],temp[1], self.AC_orientation[count]]
            count = count + 1
        return self.Bot,self.f_no
