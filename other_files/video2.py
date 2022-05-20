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

def nothing(x):
    pass

def size_mod(img,times):
    h,w = img.shape[:2]
    dim = (int(w/times), int(h/times))
    return cv2.resize(img, dim)
class vdo_tbar:
    def __init__(self,img):
        self.img = img
        cv2.namedWindow("Trackbars")

        cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
        cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
        cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
        cv2.createTrackbar("U - H", "Trackbars", 0, 179, nothing)
        cv2.createTrackbar("U - S", "Trackbars", 0, 255, nothing)
        cv2.createTrackbar("U - V", "Trackbars", 0, 255, nothing)        

    
        while True:
            frame = self.img.copy()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            l_h = cv2.getTrackbarPos("L - H", "Trackbars")
            l_s = cv2.getTrackbarPos("L - S", "Trackbars")
            l_v = cv2.getTrackbarPos("L - V", "Trackbars")
            u_h = cv2.getTrackbarPos("U - H", "Trackbars")
            u_s = cv2.getTrackbarPos("U - S", "Trackbars")
            u_v = cv2.getTrackbarPos("U - V", "Trackbars")

            lower_blue = np.array([l_h, l_s, l_v])
            upper_blue = np.array([u_h, u_s, u_v])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)

            # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # hls = cv2.cvtColor(rgb, cv2.COLOR_BGR2HLS)
            # mask = cv2.inRange(hls, lower_blue, upper_blue)
            # cv2.imshow("rgb", rgb)
            # cv2.imshow('img', frame)
            cv2.imshow('hsv', self.img)
            cv2.imshow("mask", mask)
            # cv2.imshow("hls", hls)

            key = cv2.waitKey(1)
            if key == 27:
                cv2.destroyAllWindows()
                break
