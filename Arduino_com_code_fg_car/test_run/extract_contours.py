import cv2
import numpy as np 
import imutils


class ExtractContour:
    def __init__(self,img):
        self.img = img
        H,W = self.img.shape[:2]
        #purple_mask
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        pruple_mask = cv2.inRange(hsv,(130, 100, 100), (180, 255,255))
        
        #for analysis only
        #comment at end
        #dim = (int(W/2), int(H/2))
        #pruple_mask= cv2.resize(pruple_mask, dim)
        
        kernel = np.ones((5,5),np.uint8)
        eroded = cv2.morphologyEx(pruple_mask, cv2.MORPH_OPEN, kernel)
        blur = cv2.blur(eroded, (3,3))
        eroded = cv2.erode(pruple_mask, kernel)
#        cv2.imshow('eroded_img', eroded)
#        cv2.imshow('blur', blur)
#        cv2.waitKey()
#        cv2.destroyAllWindows()


        #canny edges
        edge = cv2.Canny(blur, 10,250)
        
        ##after morph open these are not required
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        #edge = cv2.morphologyEx(edge, cv2.MORPH_CLOSE, kernel)
        #cv2.imshow('ExtractCoutour_pruple_mask',pruple_mask)
        #cv2.imshow('ExtractCoutour_edge',edge)
        #cv2.waitKey()
        #cv2.destroyAllWindows()

        (cnts, _) = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        idx = 0         
        self.bot_img = []
        self.bot_location = []
        for c in cnts: 
            x,y,w,h = cv2.boundingRect(c) 
            if w> (0.02*W) and h> (0.02*W): 
                idx+=1 
                location = [y+ h/2, x+ w/2]
                self.bot_location.append(location)
                new_img=self.img[y-20:y+h+20,x-20:x+w+20] 
                self.bot_img.append(new_img)
 #               cv2.imshow(f'{idx}bot_img_extract_contour',new_img)
 #       print('number of bots: '+ str(len(self.bot_img)))
 #       cv2.waitKey()
 #       cv2.destroyAllWindows()
                
    def ret(self):
        return self.bot_img, self.bot_location