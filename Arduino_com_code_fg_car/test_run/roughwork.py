# original lib
import cv2 
import time
import imutils
import numpy as np

import argparse

# my lib
from shape_det import ShapeDetector
from contour_finder import C_T_iden_fn
from grid_maker import GridMaker
from right_rotate import RotateImage
from image_adjuster import Alignimage


######################
# old images
# loading and resizing image
#img_main = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/GRiD_2.png')
#img = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/rotated_1.png')
#iden_task = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/Iden_task.png')
######################
#new images
img_main = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/GRiD_mod.png')
img = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/GRiD_rotated_mod.png')
iden_task = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/GRiD_mod_iden.png')



height, width = iden_task.shape[:2]
scale_percent = 25 # percent of original size
width = int(iden_task.shape[1] * scale_percent / 100)
height = int(iden_task.shape[0] * scale_percent / 100)
dim = (width, height)
iden_task = cv2.resize(iden_task, dim, interpolation = cv2.INTER_AREA)


## size of image finder
h, w = img.shape[:2]

# pi/2 rotation if requires
ri = RotateImage(img)
rotated_img = ri.SqCenter()

# finding bot_id using shapes to binary
sd = ShapeDetector()
gd = GridMaker(rotated_img)
height, weight = gd.GridVal()
bot_id = gd.IdFinder()
print(bot_id)

## purple mask
hsv = cv2.cvtColor(iden_task, cv2.COLOR_BGR2HSV)
purple_mask = cv2.inRange(hsv, (140, 25, 25), (160, 255,255))
#cv2.imshow('mask',purple_mask)
#cv2.waitKey()
##########################################
#gray=cv2.cvtColor(purple_mask,cv2.COLOR_BGR2GRAY) 
#cv2.imshow("gray",gray) 
#cv2.waitKey(0) 

edged = cv2.Canny(purple_mask, 10, 250) 
#cv2.imshow("edged",edged) 
#cv2.waitKey(0) 

(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
idx = 0 
individual_bot = []
for c in cnts: 
	x,y,w,h = cv2.boundingRect(c) 
	if w>50 and h>50: 
		idx+=1 
		new_img=iden_task[y:y+h,x:x+w] 
		individual_bot.append(new_img)
		

  
## allign image 

imReference = img_main.copy()

im = individual_bot[0]
hei, wid = im.shape[:2]
im = cv2.resize(im, (int( im.shape[1]*5) , int(im.shape[0]*5)))
cv2.imshow('winname', im)
cv2.waitKey()

ai = Alignimage(im, imReference)
imReg, h = ai.alignImages()
cv2.imshow('outFilename', imReg)
cv2.waitKey()



#cv2.imshow("im",iden_task) 
#cv2.waitKey(0) 
#cv2.destroyAllWindows()
#images are extracted 
##########################################


#####
#create a package that can rotate the image as per input from above
#
#use the online algo from whatsapp OHM for cropping bot img
#find a way to auto rotate it 
# one hard code way is using bound rectangle on cnts of cropped 
# for min rectange area the image will be correctly alligned  
#####
