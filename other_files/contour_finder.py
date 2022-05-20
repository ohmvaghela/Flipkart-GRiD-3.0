##mew
import cv2
import numpy as np

class C_T_iden_fn:
    def __init__(self,img):
        self.img = img
        self.area = []
        self.i = 0
        self.contour = [] 
#        print("in contour finder")

## not in use
#    def resize(self):    
#        if (self.img.shape[0]>700) or (self.img.shape[1]>700):
#            self.img = cv2.resize(self.img, (int( self.img.shape[1]*0.5) , int(self.img.shape[0]*0.5)))
#        return(self.img)
   
    def contour_finder(self):
        kernel = np.ones((10,10),np.float32)/100
        imgray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(imgray, (5,5), 0)
        ret, thresh = cv2.threshold(blurred, 100,255, cv2.THRESH_BINARY)
        self.contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #return print(contours)
       
#        cv2.drawContours(self.img, self.contours, -1, (0,0,0))
#        cv2.imshow("gray",imgray)
#        cv2.imshow("thresh", thresh)
#        cv2.imshow("contour", self.img)
        return(self.contours)    

    def area_list(self):
        self.i = 0
        while True:
            try:
                self.area.append(cv2.contourArea(self.contours[self.i]))  
                self.i = self.i + 1  
            except IndexError:
                break
        return self.i, self.area
    


