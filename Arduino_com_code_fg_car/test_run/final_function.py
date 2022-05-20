##bot coordinate are not accurate
# original lib
import cv2 
import time
import imutils
import numpy as np

import argparse

# my lib
#from align_bot import Alignimage
from align_tester import Alignimage
from contour_finder import C_T_iden_fn
#from extract_bot import ExtractBot
from extract_contours import ExtractContour
from grid_maker import GridMaker
from right_rotate import RotateImage
#from image_adjuster import AlignimageADJ
from shape_det import ShapeDetector
from angle import Angle


class BotFinder:
    def __init__(self,img=None):
        self.img = img
        self.BotID = []
        self.bot_angle = []
        self.Bot = {}
        self.AC_orientation = []
        ####################################
        ## extract all the images with center coordinate

    def update_image(self,image):
        self.img = image
    
    def detect_bots(self):
        ext = ExtractContour(self.img)
        bot_img,self.bot_location = ext.ret()

#        results
#        for i in range(len(bot_img)):
#           cv2.imshow(f'{i}', bot_img[i])
#        cv2.waitKey()
#        
#       for i in range(len(bot_location)):
#           loc = (int(bot_location[i][0]),int(bot_location[i][1]))
#           print(loc)
#           iden_task = cv2.circle(iden_task, loc,radius=5,
#            color=(0, 0, 255), thickness=-1)
#       
#       cv2.imshow('circle_imgs', iden_task)
#       cv2.waitKey()

####################################
# align image

        #img_align = cv2.resize(img_align, (int( img_align.shape[1]*0.5) , int(img_align.shape[0]*0.5)))
        aligned_images = []
        sd = ShapeDetector()
        
        
        for i in range(len(bot_img)):
            #allign bot
#            print('resize')
#            cv2.imshow('bot_img',bot_img[i])
#            cv2.waitKey()
            bot_img[i] = cv2.resize(bot_img[i], (int( bot_img[i].shape[1]*4) , int(bot_img[i].shape[0]*4)))            
#            print('align')
#            cv2.imshow('bot_img',bot_img[i])
#            cv2.waitKey()
            
            Agl = Angle(bot_img[i])
            degree = Agl.ret()
            self.AC_orientation.append(degree)
            #print(degree)
            Align = Alignimage(bot_img[i])
            aligned_images = Align.ret()
            

##dont use  #aligned_images,angle = Align.ret()
            
            

#            cv2.imshow('unalligned', bot_img[i])
#            cv2.imshow('aligned', aligned_images)
#            cv2.waitKey()
#            cv2.destroyAllWindows()
            #extract exact bot image
#            print('extract')


            
            
#            print(f'botshape{aligned_images.shape[:2]}')            
#            cv2.imshow('bot_list',aligned_images)
#            cv2.waitKey()

#            itr = len(bot_list)
#            for i in range(itr):
#                cv2.imshow(f'{i}',bot_list[i-1])
#            cv2.waitKey()
#            print('rotate')

            ri = RotateImage(aligned_images)
            rot_90_after,rotate_right_angle = ri.SqCenter()
            
            

#            print(f'rotate right :{rotate_right_angle}')
#            cv2.imshow('after_90_rotation', rot_90_after)
#            cv2.waitKey()
#            cv2.destroyAllWindows()
#            print('grid')
            gd = GridMaker(rot_90_after)
            bot_id = gd.IdFinder()
            
            

#            print(f'bot_id : {bot_id}')
            self.BotID.append(bot_id)
#            print(f'bot ID: {self.BotID}')
#            print(f'bot location: {self.bot_location[i]}')
            self.Bot[str(bot_id)] = self.bot_location[i]
#            print(f'loop ends\n total angle = {angle+rotate_right_angle}')
            #self.AC_orientation.append(int(angle)+int(rotate_right_angle))
    
    def get_bot_poses(self):    
        #print(self.AC_orientation)    
        #print(self.AC_orientation)
        count = 0
        for i in self.Bot.keys():
            temp = self.Bot[i]
            self.Bot[i] = [temp[0],temp[1], self.AC_orientation[count]]
            count = count + 1
        return self.Bot
#        return self.Bot,self.AC_orientation

