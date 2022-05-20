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
from Samarth_CNN.shape_identifier import ShapeIdentifier

shape_identifier = ShapeIdentifier()

class BotFinder:
    def __init__(self):#,f_no):

        self.bot_ID_all = []# all bot's ID are stored here
        self.AC_orientation = []# all bot's Angle are stored here
        self.Bot = {} # contain value as (X,Y,Theta) with key as bot ID
        self.rotated_img = 0 # temp. rotated image

    def give_frame(self,img):# provide current frame as img
        self.img = img
        self.bot_location = []# location of all bots in (X,Y)

        ext = ExtractContour(self.img)# process frame
        bot_img, self.bot_location = ext.ret()# gives croped_img, croped_img_location

        #iterate for 4 croped images        
        for i in range(len(bot_img)):
            
            #resize image 4 times original image
            h,w = bot_img[i].shape
            dim = ( int(w*4) , int(h*4) )
            bot_img[i] = cv2.resize(bot_img[i], dim)            
   
            # find angle of alignment of bot with +ve x-aixs 'degree'
            # stores the rotated image to 'self.rotated_img'
            Agl = Angle(bot_img[i])# feed croped image 
            # return bot allignment in degree and rotated croped image
            degree,self.rotated_img = Agl.ret()
            self.AC_orientation.append(degree)# add the orientation to self.AC_orientation list

            # give 4 images of croped image 
            # which will be feed to CNN
            gd = GridMaker(self.rotated_img)
            shape_imgs= gd.ShapeImages()

            # initialize temp bot id as 'self.curr_bot_id'
            self.curr_bot_id = ''
            # iterate for 4 parts of croped image
            for j in range(4):
                try: # if the entire shape is empty so 0
                    if shape_imgs[j] == None:
                        # print('empty')
                        self.curr_bot_id+=str(0)
                        continue
                except:pass
                # convert save image and load with matplotlib's plot function
                cv2.imwrite('useless_file.png', shape_imgs[j])
                in_img = plt.imread('useless_file.png')
                # feed the shape to CNN indentifier
                shape = shape_identifier.predict(in_img)
                if shape == 0:# ID for circle is 2 
                    # print('circle')
                    self.curr_bot_id+=str(2)
                elif shape == 1:# ID for circle is 1 
                    # print('triangle')
                    self.curr_bot_id+=str(1)

            # add the temp bot ID to main list of bot_ID 
            self.bot_ID_all.append(self.curr_bot_id)    
            # add bot location and orientation to self.Bot dict with ID string as key
            self.Bot[self.curr_bot_id] = [self.bot_location[i][0], self.bot_location[i][1]
                                            , self.AC_orientation[i]]
        e = time.time()
        print(s-e)
    def ret(self):    
        # count = 0
        # for i in self.Bot.keys():
        #     temp = self.Bot[i]
        #     self.Bot[i] = [temp[0],temp[1], self.AC_orientation[count]]
        #     count = count + 1
        return self.Bot

# if __name__ == '__main__':
    # feed = cv2.imread(f'C:/Users/OHM/Desktop/pytthon/error_imgs/{63}.jpg')
    # BF = BotFinder()
    # for i in range(5):
    #    BF.give_frame(feed)
    #    bot = BF.ret()
