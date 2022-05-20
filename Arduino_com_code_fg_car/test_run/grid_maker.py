import cv2
import numpy as np
from shape_det import ShapeDetector
from contour_finder import C_T_iden_fn


class GridMaker:
    def __init__(self, img):
        self.img = img
        self.sd = ShapeDetector()
        self.bot_id = []
        self.h, self.w = self.img.shape[:2]
        self.id_str = ""
        
        kernel = np.ones((9,9), np.uint8)
        erode_img = cv2.erode(self.img, kernel, iterations = 2)
        #dilate_img = cv2.dilate(erode_img, kernel, iterations = 2)
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gradient = cv2.morphologyEx(erode_img, cv2.MORPH_CLOSE, kernel)
        #img = cv2.


        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        im = cv2.filter2D(self.img, -1, kernel)

        hsv = cv2.cvtColor(gradient, cv2.COLOR_BGR2HSV)
        yellow_mask = cv2.inRange(hsv, (20,100,100), (40,255,255) )#def 25
        imask = yellow_mask>0
        self.yellow = np.zeros_like(img, np.uint8)
        self.yellow[imask] = img[imask]        
        self.bot_no = 0


#        print('present in grid maker')
#        cv2.imshow("erode",erode_img)
#        #cv2.imshow("dilate",dilate_img)
#        cv2.imshow("graditent",gradient)
#        cv2.imshow("im",im)
#        
#        cv2.imshow('img',self.img)
#        cv2.imshow('yellow_mask',yellow_mask)
#        cv2.imshow('after_mask',self.yellow)
#        cv2.waitKey()
#        cv2.destroyAllWindows()

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

    def SectionID(self,id):
        X,W,Y,H = self.rect_egdes(int(id))
        #crop = self.yellow[ int(Y)+20:int(H)-20, int(X)+20:int(W)-20 ]
        crop = self.yellow[ int(Y):int(H), int(X):int(W) ]

        fn = C_T_iden_fn(crop)
        cnts = fn.contour_finder()
        try :
            shape = self.sd.detect(cnts[0])
            shape_ID = self.ShapeToID(shape)
#
#            print(f'{shape_ID}:{shape}')
#
        except IndexError:
            shape_ID = 0
#
#        cv2.imshow('crop',crop)
#        cv2.waitKey()
#
        return shape_ID 

    def IdFinder(self):
        for i in range(4):
#            print(self.SectionID(i))
            self.bot_id.append(self.SectionID(i))
        for i in range(4):
            exp = 10**i
            #self.bot_no += self.bot_id[i] * exp
            self.id_str += str(self.bot_id[i])
#            print(self.id_str)
#           
#            print(self.bot_id)
#
            
#        return self.bot_no
        return self.id_str