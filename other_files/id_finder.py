import cv2
import numpy as np
from shape_det import ShapeDetector
from contour_finder import C_T_iden_fn
global image_path
image_path = r'C:/Users/OHM/Desktop/pytthon/error_imgs/'


class GridMaker:
    def __init__(self, img):
        self.img = img
        self.sd = ShapeDetector()
        self.BW_Shape = []        
        self.h, self.w = self.img.shape[:2]
        self.id_str = ""

        #first erode
        kernel = np.ones((9,9), np.uint8)
        erode_img = cv2.erode(self.img, kernel, iterations = 2)## original iterations = 2
        # cv2.imshow(f'erode{self.number}', erode_img)
        
        #convert HSV and mask yellow color 
        hsv = cv2.cvtColor(erode_img, cv2.COLOR_BGR2HSV)
        self.yellow_mask = cv2.inRange(hsv, (15,100,100), (45,255,255) )        
        imask = self.yellow_mask>0
        self.yellow = np.zeros_like(img, np.uint8)
        self.yellow[imask] = img[imask]        
        # cv2.imshow('mask', self.yellow_mask)
        # cv2.imshow(f'yellow{self.number}', self.yellow)
 
        #Second erode
        kernel = np.ones((9,9),np.uint8)
        self.yellow = cv2.erode(self.yellow, kernel)
        self.bot_no = 0
        # cv2.imshow('final_erode',self.yellow)
        # print(self.yellow.shape)
        
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        

    def ShapeToID(self,shape_str):
        if shape_str == "triangle":
            return 1
        elif shape_str == "circle":
            return 2

    def rect_egdes(self,id):
        X = 0
        W = 0
        Y = 0
        H = 0
        if id == 0:
            X = 0
            W = self.w/2
            Y = 0
            H = self.h/2
        elif id == 1:
            X = 0
            W = self.w/2
            Y = self.h/2
            H = self.h
        elif id == 2:
            X = self.w/2
            W = self.w
            Y = self.h/2
            H = self.h
        elif id == 3:
            X = self.w/2
            W = self.w
            Y = 0
            H = self.h/2
        return X,W,Y,H

    def Section(self,id):
        X,W,Y,H = self.rect_egdes(int(id))
        #crop = self.yellow[ int(Y)+20:int(H)-20, int(X)+20:int(W)-20 ]
        crop = self.yellow_mask[ int(Y):int(H), int(X):int(W) ]
        crop = cv2.resize(crop, (100,100))
        _,thresh = cv2.threshold(crop, 10, 255, cv2.THRESH_BINARY_INV)
        cnts,_ = cv2.findContours(crop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # print(len(cnts))
        if len(cnts) == 0:
            thresh = None
        return thresh

    def ShapeImages(self):
        for i in range(4):
            self.BW_Shape.append(self.Section(i))
        return self.BW_Shape    
        