import cv2
import numpy as np
from shape_det import ShapeDetector
from contour_finder import C_T_iden_fn
global image_path
image_path = r'C:/Users/OHM/Desktop/pytthon/error_imgs/'


class GridMaker:
    def __init__(self, img,f_no,number):
        self.img = img
        self.f_no = f_no
        self.number = number
        self.sd = ShapeDetector()
        self.bot_id = []
        self.h, self.w = self.img.shape[:2]
        self.id_str = ""

        # cv2.imshow('img', self.img)
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        im = cv2.filter2D(self.img, -1, kernel) 
        # cv2.imshow(f'img{self.number}', self.img)
        ## trying to sharpen image

        kernel = np.ones((9,9), np.uint8)
        erode_img = cv2.erode(self.img, kernel, iterations = 2)## original iterations = 2
        # cv2.imshow(f'erode{self.number}', erode_img)
        hsv = cv2.cvtColor(erode_img, cv2.COLOR_BGR2HSV)
        
        self.yellow_mask = cv2.inRange(hsv, (15,100,100), (45,255,255) )        
        imask = self.yellow_mask>0
        self.yellow = np.zeros_like(img, np.uint8)
        self.yellow[imask] = img[imask]        
        # cv2.imshow('mask', self.yellow_mask)
        # cv2.imshow(f'yellow{self.number}', self.yellow)
 
        #final erode
        kernel = np.ones((9,9),np.uint8)
        self.yellow = cv2.erode(self.yellow, kernel)
        # cv2.imshow('final_erode',self.yellow)
        self.bot_no = 0
        # print(self.yellow.shape)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        f_name = f'bot_BGR/{(4*self.f_no) + self.number}.png'     
        cv2.imwrite(f_name, self.img)
#        print('present in grid maker')
        
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

    def SectionID(self,id):
        X,W,Y,H = self.rect_egdes(int(id))
        #crop = self.yellow[ int(Y)+20:int(H)-20, int(X)+20:int(W)-20 ]
        crop = self.yellow_mask[ int(Y):int(H), int(X):int(W) ]
        H,W = crop.shape[:2]
        area = H*W
        cntrs,_ =cv2.findContours(crop, 
            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        #cv2.drawContours(crop, cnts, -1, (255,0,0),thickness=4)
                
        try :
            c = max(cntrs,key = cv2.contourArea)  
            max_cnt_area = cv2.contourArea(c)
#
            # print(f'contour Area {max_cnt_area} || area : {0.04*area}')
#                                     
            if max_cnt_area < (0.01 * area):
                c={}
            shape = self.sd.detect(c)    
            shape_ID = self.ShapeToID(shape)
#
            # print(f'{shape_ID}:{shape}')
#
        except:
            shape_ID = int(0)
#       
        # if shape_ID == 2:
            # self.file_no = self.f_no + self.number+ int(id) 
            # cv2.imwrite(f'ML_training_set_circle/{self.file_no}.png', crop)
        # cv2.imshow('crop',crop)
        # cv2.waitKey()
        # else: self.file_no = self.f_no
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
        # return self.id_str,self.file_no