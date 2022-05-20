import cv2
import numpy as np
from contour_finder import C_T_iden_fn
import imutils
import time

img = cv2.imread('C:/Users/OHM/Desktop/pytthon/Resources/align_error.png')
cv2.imshow('img',img)
cv2.waitKey()

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
purple_mask = cv2.inRange(hsv, (140,25,25), (160,255,255) )
imask = purple_mask>0
purple = np.zeros_like(img, np.uint8)
purple[imask] = img[imask] 
edged = cv2.Canny(purple, 10, 250) 
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)) 
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

print("in Align image")
cv2.imshow('imask',purple_mask)
cv2.imshow('purple',purple)
cv2.imshow('edged',edged)
cv2.imshow('img',closed)
cv2.waitKey()
cv2.destroyAllWindows()

init_area = int(closed.shape[0]) * int(closed.shape[1]) + 1
increase = False
init_angle = 0
for angle in np.arange(0, 370, 1):
    rotated = imutils.rotate_bound(closed, angle) 
    cnts, asa = cv2.findContours(rotated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key = cv2.contourArea)
    [x,y,w,h] = cv2.boundingRect(c)
    #cv2.rectangle(rotated,(x,y),(x+w,y+h),(0,255,0),thickness = 5)

    #area = abs( (x-w) * (y-h))
    area_2 = cv2.contourArea(c)
    #cv2.drawContours(rotated, cnts, -1, color = (255,0,0))

    area = abs( (w) * (h))
    print(f'prev {init_area} || {area}  shape:{rotated.shape[0]*rotated.shape[1]}')
    #if area > init_area and increase:
    #    break
    if area < init_area :
        init_area = area
        init_angle = angle
        
    cv2.imshow('rotated',rotated)
    cv2.waitKey(1)
rotated = imutils.rotate_bound(img, init_angle)
print(f'angle ={init_angle}')
cv2.imshow('final_img',rotated)
cv2.waitKey()
cv2.destroyAllWindows()
print("out of align image")
