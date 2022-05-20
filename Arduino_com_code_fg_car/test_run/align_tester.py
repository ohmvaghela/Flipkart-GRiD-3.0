import numpy as np
import cv2 
import imutils


class Alignimage:

    def __init__(self,img):
        self.img = img
        temp = self.img.copy()
        cv2.destroyAllWindows()
        #img to square
        hsv = cv2.cvtColor(temp, cv2.COLOR_BGR2HSV)
        purple_mask = cv2.inRange(hsv, (130,100,100), (180,255,255) )
        imask = purple_mask>0
        purple = np.zeros_like(temp, np.uint8)
        purple[imask] = temp[imask] 
        edged = cv2.Canny(purple, 10, 250) 
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)) 
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        _, thresh = cv2.threshold(closed, 200, 255, cv2.THRESH_BINARY)
        countours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        zero = np.zeros_like(temp, np.float32)
        c = max(countours, key = cv2.contourArea)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(zero,[box],0,(0,0,255),2)
        gray = cv2.cvtColor(zero, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, (5,5))

#        cv2.imshow('1img',self.img)
#        cv2.imshow('2purple_mask',purple_mask)
#        cv2.imshow('3purple',purple)
#        cv2.imshow('4edged',edged)
#        cv2.imshow('5closed',closed)
#        cv2.imshow('6thresh',thresh)
#        cv2.imshow('7zero',zero)
#        cv2.imshow('8gray',gray)
#        cv2.waitKey()
#        cv2.destroyAllWindows()

        #find edge points
        dst = cv2.cornerHarris(gray,5,3,0.04)
        _,dst = cv2.threshold(dst, 0.1*dst.max(),255,0)
        dst = np.uint8(dst)
        _,_,_,centroid = cv2.connectedComponentsWithStats(dst)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER,100,0.001)
        corners = cv2.cornerSubPix(gray, np.float32(centroid), (5,5), (-1,-1), criteria)
        inpt_points = []
        for i in corners:
            point = ( int(i[0]) , int(i[1]) )
            #zero = cv2.circle(zero, point, radius=0, color=(255, 255, 255), thickness=5)
            x = i[0]
            y = i[1]
            pnt = [int(x),int(y)]
            inpt_points.append(pnt)

#            cv2.imshow('point', zero)
#            cv2.waitKey()
#        cv2.destroyAllWindows()

        h,w = zero.shape[:2]
#        print(f'before : \n{inpt_points}')
        inpt_points.pop(0)
#        print(f'after  : \n{inpt_points}')
        # orientation 
        # 1 --> top-left
        # 2 --> top-right
        # 3 --> bottom-right
        # 4 --> bottom-left
        if inpt_points[1][0] < w*0.5:
            # a --> third point
#            print("True")
            a = inpt_points[2]
            inpt_points[2] = inpt_points[1]
            inpt_points[1] = a
        
        #tranform image 
        opt_points = [[0,0], [w,0], [0,h], [w,h] ]
        input_points =  np.float32(inpt_points)
        output_points =  np.float32(opt_points)
#        print('output points')
#        print(output_points)
#        print('inpt_points')
#        print(input_points)
        matrix = cv2.getPerspectiveTransform(input_points, output_points)
        output_img = cv2.warpPerspective(self.img, matrix, (w,h))
        self.rotated = output_img.copy()
#        cv2.imshow('input_img', self.img)
#        cv2.imshow('output_img', output_img)
#        cv2.waitKey() 

    def ret(self): 
        return self.rotated#,self.init_angle