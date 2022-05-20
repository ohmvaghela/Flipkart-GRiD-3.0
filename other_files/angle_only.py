# original lib
import cv2 
import time
import imutils
import numpy as np
import argparse
import matplotlib.pyplot as plt

# my lib
from extract_contours import ExtractContour
from id_finder import GridMaker
from angle import Angle
# from Samarth_CNN.shape_identifier import ShapeIdentifier

# shape_identifier = ShapeIdentifier()

class BotFinder:
    def __init__(self):#,f_no):

        self.bot_ID_all = []# all bot's ID are stored here
        self.Bot = {} # contain value as (X,Y,Theta) with key as bot ID
        self.orientation = 0# angle of orientation
        self.rotated_img = 0 # temp. rotated image

    def give_frame(self,img):# provide current frame as img
        self.img = img
        self.bot_location = []# location of all bots in (X,Y)

        ext = ExtractContour(self.img)# process frame
        bot_img, self.bot_location = ext.ret()# gives croped_img, croped_img_location

        #resize image 4 times original image
        
        print(bot_img.shape[:2])
        h,w = bot_img.shape[:2]
        dim = ( int(w*4) , int(h*4) )
        bot_img = cv2.resize(bot_img, dim)            

        # find angle of alignment of bot with +ve x-aixs 'degree'
        # stores the rotated image to 'self.rotated_img'
        Agl = Angle(bot_img)# feed croped image 
        # return bot allignment in degree and rotated croped image
        self.orientation,self.rotated_img = Agl.ret()
        
    def ret(self):    
        self.Bot = [self.orientation, self.bot_location]
        return self.Bot

# if __name__ == '__main__':
#     feed = cv2.imread(f'C:/Users/OHM/Desktop/pytthon/error_imgs/{63}.jpg')
#     BF = BotFinder()
#     for i in range(5):
#        BF.give_frame(feed)
#        bot = BF.ret()
