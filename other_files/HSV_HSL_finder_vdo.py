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


cam_feed1 = cv2.imread('Resources/cam_feed_1.jpeg')
cam_feed2 = cv2.imread('Resources/cam_feed_2.jpeg')
cam_feed3 = cv2.imread('Resources/cam_feed_2.jpeg')
fil = cv2.imread('ring_light.jpg')

#cap = cv2.VideoCapture('C:/Users/OHM/Desktop/pytthon/Resources/final_arean_1.mp4')
#_,frame = cap.read()
cam_feed4 = cv2.imread('Resources/photo10.jpg')
cam_feed3 = fil.copy()
#cam_feed3 = cv2.rotate(cam_feed3, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
h,w = cam_feed3.shape[:2]
dim = (int(w/3), int(h/3))
cam_feed3 = cv2.resize(cam_feed3, dim)


def nothing(x):
    pass

#cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")

cv2.createTrackbar("L - H", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - L", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - L", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("epsilon", "Trackbars", 0, 50, nothing)


while True:
    copy_img = cam_feed3.copy()
    hsv = cv2.cvtColor(copy_img, cv2.COLOR_BGR2HLS)
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - L", "Trackbars")
    l_v = cv2.getTrackbarPos("L - S", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - L", "Trackbars")
    u_v = cv2.getTrackbarPos("U - S", "Trackbars")
    #l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    #l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    #l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    #u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    #u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    #u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    epsillon = cv2.getTrackbarPos("epsilon", "Trackbars")
    epsillon_val = epsillon/100
    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])
    

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    blur = cv2.GaussianBlur(mask, (5,5), 0)
    
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    
    blur = cv2.GaussianBlur(thresh, (5,5), 0)
    

    kernel = np.ones((5,5), np.uint8)
    opening = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel)
    
    #img_erosion = cv2.erode(blur, kernel, iterations=1)
    #img_dilation = cv2.dilate(blur, kernel, iterations=5)
    #print("dilated inage")

    #test(img_dilation,'img_dilation')

    contours, _ = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    area = cam_feed3.shape[:2][1]*cam_feed3.shape[:2][0]
    min_area = area/(10*20)
    print('start')
    i = 0
    boxes = {}
    coord = []
    for c in contours:

        cnt_area = cv2.contourArea(c)
        #if cnt_area > min_area/5 and cnt_area < 10* min_area:
        peri = cv2.arcLength(c, True)
        #approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        approx = cv2.approxPolyDP(c, epsillon_val * peri, True)

        
        if cnt_area > 2250 and cnt_area < 6300 and len(approx) == 4:
            i +=1
            #cv2.drawContours(cam_feed3, c, -1, (0,255,0),thickness=5)
            #print(f'{area} || {min_area} || {cnt_area} ')

            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            center_location = (cX,cY)
            boxes[i] = {center_location: True}
            coord.append(center_location)
            # draw the contour and center of the shape on the image
            cv2.drawContours(copy_img, [c], -1, (0, 255, 0), 2)
            cv2.circle(copy_img, (cX, cY), 30, (255, 255, 0), 4)
            cv2.circle(copy_img, (cX, cY), 4, (255, 0, 255), -1)
            cv2.putText(copy_img, str(i), (cX - 20, cY - 20),
        	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    
    


    
    
    #result = cv2.bitwise_and(cam_feed3, cam_feed3, mask=mask)
    #cnt,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(result, cnt,-1, (0,0,255),thickness=5)
    cv2.imshow("cam_feed3", copy_img)
    cv2.imshow("mask", mask)
    #cv2.imshow("result", result)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()