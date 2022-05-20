import cv2
import numpy as np
from contour_finder import C_T_iden_fn
import imutils
import time


for i in range(6300):
    try:
        path = f'C:/Users/OHM/Desktop/pytthon/colored_bot/0122/{i}.png'
        temp = cv2.imread(path)
        # cv2.imshow('winname', temp)
        print(i)
        resize = cv2.resize(temp, (100,100))
        cv2.imwrite(path, resize)
    except:pass

for i in range(12500):
    try:
        path = f'C:/Users/OHM/Desktop/pytthon/colored_bot/2210/{i}.png'
        temp = cv2.imread(path)
        # cv2.imshow('winname', temp)
        print(i)
        resize = cv2.resize(temp, (100,100))
        cv2.imwrite(path, resize)
    except:pass
    
for i in range(12500):
    try:
        path = f'C:/Users/OHM/Desktop/pytthon/colored_bot/2122/{i}.png'
        temp = cv2.imread(path)
        # cv2.imshow('winname', temp)
        print(i)
        resize = cv2.resize(temp, (100,100))
        cv2.imwrite(path, resize)
    except:pass

for i in range(12500):
    try:
        path = f'C:/Users/OHM/Desktop/pytthon/colored_bot/2010/{i}.png'
        temp = cv2.imread(path)
        # cv2.imshow('winname', temp)
        print(i)
        resize = cv2.resize(temp, (100,100))
        cv2.imwrite(path, resize)
    except:pass
    