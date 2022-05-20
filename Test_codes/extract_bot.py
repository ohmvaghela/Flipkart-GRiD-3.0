import cv2
import numpy as np

from contour_finder import C_T_iden_fn

class ExtractBot:
    def __init__(self, img):
        self.img = img
#        cv2.destroyAllWindows()
        self.W, self.H = self.img.shape[:2]

    def BotImg(self):
        #purple mask
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        purple_mask = cv2.inRange(hsv, (140,25,25), (160,255,255) )
        
        #canny edge img
        edged = cv2.Canny(purple_mask , 10, 255) 
#        cv2.imshow('Extract_bot_PPle_mask',purple_mask)
#        cv2.imshow('Extract_bot_edged',edged)
        (cnts, _) = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,
         cv2.CHAIN_APPROX_SIMPLE)
        Bots_list = []
        idx = 0
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            if w>(0.1*self.W) and h> (0.1*self.W): 
                idx+=1 
                new_img=self.img[y:y+h,x:x+w]         
                Bots_list.append(new_img)
                cv2.imshow('new_img_extract_bot', new_img)
#                print(len(Bots_list))
#        cv2.waitKey()
#        cv2.destroyAllWindows()
        return Bots_list