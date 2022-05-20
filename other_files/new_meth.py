##bot coordinate are not accurate
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
from extract_bot import ExtractBot
from align_bot import Alignimage
from extract_contours import ExtractContour

#img import
img_main = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/GRiD_mod.png')
img_align = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/GRiD_rotated_mod.png')
iden_task = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/GRiD_mod_iden.png')
iden_task_huge = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/Iden_task_huge.png')
arena = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/arena.jpeg')
arena_high = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/arena_high.png')
rot_90 = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/GRiD_mod_90_rot.png')
with_empty = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/GRiD_mod_with_empty.png')
deformed_GRiD = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/deformed_GRiD.png')
cv2.imshow('winname', arena)
cv2.waitKey()

##shape Iden task
height, width = iden_task.shape[:2]
scale_percent = 25 # percent of original size
width = int(iden_task.shape[1] * scale_percent / 100)
height = int(iden_task.shape[0] * scale_percent / 100)
dim = (width, height)
iden_task = cv2.resize(iden_task, dim, interpolation = cv2.INTER_AREA)


## rotate by an angle not 90deg
## make grid and shape dect

####################################
## extract all the images with center coordinate
start = time.time()
ext = ExtractContour(arena_high)
bot_img,bot_location = ext.ret()
end = time.time()
print(f'ExtractContour {end-start}')
# results
#for i in range(len(bot_img)):
#    cv2.imshow(f'{i}', bot_img[i])
#cv2.waitKey()
#
#for i in range(len(bot_location)):
#    loc = (int(bot_location[i][0]),int(bot_location[i][1]))
#    print(loc)
#    iden_task = cv2.circle(iden_task, loc,radius=5,
#     color=(0, 0, 255), thickness=-1)
#
#cv2.imshow('circle_imgs', iden_task)
#cv2.waitKey()

####################################
# align image

#img_align = cv2.resize(img_align, (int( img_align.shape[1]*0.5) , int(img_align.shape[0]*0.5)))
aligned_images = []
sd = ShapeDetector()
BotID = []
Start = time.time()
for i in range(len(bot_img)):
    #allign bot
    start = time.time()
    
    Align = Alignimage(bot_img[i])
    aligned_images = Align.ret()
    end = time.time()
    print(f'align image {end-start}')

#    cv2.imshow('unalligned', bot_img[i])
#    cv2.imshow('aligned', aligned_images)
#    cv2.waitKey()
#   extract exact bot image
    start = time.time()

    extrectbot = ExtractBot(aligned_images)
    bot_list = extrectbot.BotImg()
    #cv2.imshow('bot_list', bot_list[0])
    end = time.time()
    print(f'extract bot {end-start}')

#    itr = len(bot_list)
#    for i in range(itr):
#        cv2.imshow(f'{i}',bot_list[i-1])
#    cv2.waitKey()
    bot_list[0] = cv2.resize(bot_list[0], (int( bot_list[0].shape[1]*4) , int(bot_list[0].shape[0]*4)))
#    cv2.imshow('rotate_img_input', bot_list[0])
#    cv2.waitKey()
    ri = RotateImage(bot_list[0])
    rot_90_after = ri.SqCenter()
    #cv2.imshow('after_90_rotation', rot_90_after)
    #cv2.waitKey()
    gd = GridMaker(rot_90_after)
    bot_id = gd.IdFinder()
    BotID.append(bot_id)
    print(f'bot ID: {BotID[i]}')
    print(f'bot location: {bot_location[i]}')
    
End = time.time()
print(f'looptime : {End-Start}')




