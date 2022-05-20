# #####
#
# https://pysource.com
#
# Tutorial: Object detection using HSV Color space – OpenCV 3.4 with python 3 Tutorial 9
#
# URL: https://pysource.com/2018/01/31/object-detection-using-hsv-color-space-opencv-3-4-with-python-3-tutorial-9/
# 
# ###


import cv2
import numpy as np


img=cv2.imread(f'C:/Users/OHM/Desktop/pytthon/error_imgs/9.jpg')

cam_feed3 = img.copy()
#cam_feed3 = cv2.rotate(cam_feed3, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
h,w = cam_feed3.shape[:2]
dim = (int(w/3), int(h/3))
#cam_feed3 = cv2.resize(cam_feed3, dim)


def nothing(x):
    pass

#cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")

cv2.createTrackbar("blk_siz", "Trackbars", 0, 50, nothing)
cv2.createTrackbar("constant", "Trackbars", 0, 50, nothing)

while True:
    copy_img = cam_feed3.copy()
    hsv = cv2.cvtColor(copy_img, cv2.COLOR_BGR2HLS)
    blk_size = cv2.getTrackbarPos("blk_siz", "Trackbars")
    constant = cv2.getTrackbarPos("constant", "Trackbars")
    

    kernel = np.ones((3,3),np.uint8)
    gradient = cv2.morphologyEx(copy_img, cv2.MORPH_GRADIENT, kernel)
    #cv2.imshow('1gradient',gradient)

    gray = cv2.cvtColor(gradient,cv2.COLOR_BGR2GRAY)
    #cv2.imshow('2gray', gray)

    #_,thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    #cv2.imshow('thresh', thresh)

    blur = cv2.GaussianBlur(gray, (7,7), 0)
    # cv2.imshow('3blur', blur)
    kernel = np.ones((3,3),np.uint8)
    dilate = cv2.morphologyEx(blur, cv2.MORPH_ERODE, kernel)
    # cv2.imshow('4dialte', dilate)
    kernel = np.ones((7,7),np.uint8)
    close_1 = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('5close1',close_1)
    kernel = np.ones((5,5),np.uint8)
    dilate = cv2.morphologyEx(close_1, cv2.MORPH_ERODE, kernel)
    cv2.imshow('dilate',dilate)
    try:
        adpt_thresh = cv2.adaptiveThreshold(dilate, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blk_size, constant)
        cv2.imshow("ad thresh",adpt_thresh)
    except:
        pass
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()