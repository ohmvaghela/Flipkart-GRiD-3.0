# region lib
import cv2 
import time
import imutils
import numpy as np
import argparse
import matplotlib.pyplot as plt
from skimage.transform import (hough_line,hough_line_peaks) 
import math

from Smarth_CNN.shape_identifier import ShapeIdentifier

# PCA tester
from collections import deque
import matplotlib.pyplot as plt
from sklearn import decomposition
import pickle
# endregion

def size_mod(img,times):
    h,w = img.shape[:2]
    dim = (int(w*times), int(h*times))
    return cv2.resize(img, dim)

def nothing(x):
    pass

def min_dist(coord_1,coord_2):
    dist = math.sqrt(  (coord_1[0] - coord_2[0])**2  + (coord_1[1] - coord_2[1])**2  )
    return dist

class ShapeDetector:
	def __init__(self):
		pass
		
	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)

		approx = cv2.approxPolyDP(c, 0.04 * peri, True)
		if len(approx) == 3: 
			shape = "triangle"
		else:
			shape = "circle"	
		return shape

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
        
class Angle:
    def __init__(self,img):
        self.ret_degree = 0 # orientation found
        self.img = img # image to be rotated
        H,W = self.img.shape[:2] # original image height 
        copy_img = self.img.copy() # copy of original image

        # change image format
        # idk why i used rgb format 
        rgb = cv2.cvtColor(copy_img, cv2.COLOR_BGR2RGB) 
        hsv = cv2.cvtColor(copy_img, cv2.COLOR_BGR2HSV)
        # cv2.imshow('rgb', rgb)
        # cv2.imshow('hsv', hsv)
        # cv2.imshow('img', self.img)
        
        # white mask of image 
        mask = cv2.inRange(hsv, (0, 0, 254), (255, 255,255))
        # cv2.imshow('mask_angle', mask)
        
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        
        # find contour
        (cnts, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        
        
        try:
            # find center of biggest contour
            c = max(cnts, key = cv2.contourArea)
            x,y,w,h = cv2.boundingRect(c)
            location = [int(y+ h/2), int(x+ w/2)]

            # assgin value of orientation in degree
            self.angle_b([H,W],location) 
            
            # draw line on bot's provided image
            copy_img = cv2.line(copy_img, (int(W/2),int(H/2)), 
                (location[1],location[0]), (255,0,0))
            # cv2.imshow('copy_img', copy_img)
            # cv2.waitKey()

        except:
            print("failed in angle detection")
            self.ret_degree = 90
            pass

    def angle_b(self,img_size,position):
        self.img_size = img_size # image size (H,W)
        self.position = position # contour center location in image
        H,W = self.img_size
        h,w = self.position

        # x,y are loaction of contour center w.r.t image center
        x = w - (W/2)
        y = (H/2) - h
        
        # rad and degree are orientation w.r.t to +ve x-axis
        rad = math.atan2(y , x)
        degree = rad*180/math.pi
        
        # assign global degre variable
        self.ret_degree = degree
        # print(f'initial_angle :: {self.ret_degree}')

    def ret(self):

        (h, w) = self.img.shape[:2] # image shape
        (cX, cY) = (w // 2, h // 2) # image center co-ord

        # rotate image such that the LED is on top center 
        M = cv2.getRotationMatrix2D((cX, cY), int(90-self.ret_degree), 1.0)
        rotated = cv2.warpAffine(self.img, M, (w, h))
        # cv2.imshow('roated', rotated)

        # working on rotated image
        # creating purple mask
        hsv = cv2.cvtColor(rotated, cv2.COLOR_BGR2HSV)
        pruple_mask = cv2.inRange(hsv,(130, 100, 80), (180, 255,255))
        # cv2.imshow('purple mask', pruple_mask)

        # processing mask
        kernel = np.ones((9,9),np.uint8)
        dilate = cv2.dilate(pruple_mask, kernel)
        edge = cv2.Canny(dilate, 10,250)
        kernel = np.ones((13,13),np.uint8)
        closed = cv2.morphologyEx(edge, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow('dilate',dilate)
        # cv2.imshow('edge',edge)
        # cv2.imshow('closed',closed)

        # find biggest contours of processed mask image
        (cnts, _) = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        c = max(cnts,key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c) 
        crop_img = rotated[y:y+h,x:x+w]
        # cv2.imshow('crop', crop_img)

        # print(f'bot orientation : {self.ret_degree}')        
        return self.ret_degree,crop_img

class ExtractContour:
    def __init__(self,img):
        self.img = img
        H,W = self.img.shape[:2]
        self.bot_img = [] # list of bot extracted images
        
        #purple_mask
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        pruple_mask = cv2.inRange(hsv,(130, 100, 80), (180, 255,255))
        # cv2.imshow('purple mask', pruple_mask)

        kernel = np.ones((5,5),np.uint8)
        opening = cv2.morphologyEx(pruple_mask, cv2.MORPH_OPEN, kernel)
        blur = cv2.blur(opening, (3,3))
        eroded = cv2.erode(pruple_mask, kernel)
        # cv2.imshow('opening', opening)
        # cv2.imshow('blur', blur)
        # cv2.imshow('eroded_img', eroded)

        #canny edges
        edge = cv2.Canny(blur, 10,250)
        small_img = size_mod(edge, 0.5)
        # cv2.imshow('egde', small_img)

        # find external contour of egde  
        (cnts, _) = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        
        self.bot_location = [] # list of bot location
        for c in cnts:
            # print(f'{cv2.contourArea(c)} |||  W : { 0.02*0.02*H*W}') 
            # find the bound rectangle of bot
            x,y,w,h = cv2.boundingRect(c) 
            if w> (0.02*W) and h> (0.02*W): 
                location = [y+ h/2, x+ w/2]
                # add loaction of current bot 
                self.bot_location.append(location)
                # crop the bot out of image
                new_img=self.img[y-30:y+h+30,x-30:x+w+30] 
                # add image of current bot 
                self.bot_img.append(new_img)
                # cv2.imshow(f'{idx}bot_img_extract_contour',new_img)
        
        # print number of bots
        # print('number of bots: '+ str(len(self.bot_img)))
                
    def ret(self):
        return self.bot_img, self.bot_location

class BotFinder:
    def __init__(self):#,f_no):
        # ID = bot_ID()# intialize PCA bot ID finder 
        self.bot_ID_all = []# all bot's ID are stored here
        self.rotated_img = 0 # temp. rotated image

    def give_frame(self,img):# provide current frame as img
        self.img = img
        self.Bot = {} # contain value as (X,Y,Theta) with key as bot ID
        self.AC_orientation = []# all bot's Angle are stored here

        self.bot_location = []# location of all bots in (X,Y)

        ext = ExtractContour(self.img)# process frame
        bot_img, self.bot_location = ext.ret()# gives croped_img, croped_img_location

        #iterate for 4 croped images        
        for i in range(len(bot_img)):
            
            # show extracted image
            # cv2.imshow('bot_img', bot_img[i])
            # cv2.waitKey()

            #resize image 4 times original image
            h,w = bot_img[i].shape[:2]
            dim = ( int(w*4) , int(h*4) )
            # print(dim)
            bot_img[i] = cv2.resize(bot_img[i], dim)            
   
            # find angle of alignment of bot with +ve x-aixs 'degree'
            # stores the rotated image to 'self.rotated_img'
            Agl = Angle(bot_img[i])# feed croped image 
            # return bot allignment in degree and rotated croped image
            degree,self.rotated_img = Agl.ret()
            self.AC_orientation.append(degree)# add the orientation to self.AC_orientation list

            # give 4 images of croped image 
            # which will be feed to CNN
            gd = GridMaker(self.rotated_img)
            shape_imgs= gd.ShapeImages()

            # initialize temp bot id as 'self.curr_bot_id'
            self.curr_bot_id = ''
            # iterate for 4 parts of croped image
            sm = time.time()
            for j in range(4):
                try: # if the entire shape is empty so 0
                    if shape_imgs[j] == None:
                        # print('empty')
                        self.curr_bot_id+=str(0)
                        continue
                except:pass
                # convert save image and load with matplotlib's plot function
                s1 = time.time()
                
                in_img = shape_imgs[j]
                e1 = time.time()
                # feed the shape to CNN indentifier
                s2 = time.time()
                shape = shape_identifier.predict(in_img)
                if shape == 0:# ID for circle is 2 
                    # print('circle')
                    # cv2.imshow('winname', in_img)
                    # cv2.waitKey()
                    self.curr_bot_id+=str(2)
                elif shape == 1:# ID for circle is 1 
                    # print('triangle')
                    self.curr_bot_id+=str(1)
                e2 = time.time()
                # print(f'saving : {(e1-s1):.5f} || model : {e2-s2:.5f} || total: {s1-e2:.5f}')
            em = time.time()
            # print(f'{(em-sm):.5f}')
            # add the temp bot ID to main list of bot_ID 
            self.bot_ID_all.append(self.curr_bot_id)    
            # add bot location and orientation to self.Bot dict with ID string as key
            self.Bot[self.curr_bot_id] = [self.bot_location[i][0], self.bot_location[i][1]
                                            , self.AC_orientation[i]]

    def ret(self):    
        # count = 0
        # for i in self.Bot.keys():
        #     temp = self.Bot[i]
        #     self.Bot[i] = [temp[0],temp[1], self.AC_orientation[count]]
        #     count = count + 1
        return self.Bot

# region PCA tester
# class bot_ID:
#     def __init__(self):
#         self.bot_ID = ''
#         filename = 'finalized_model.sav'
#         loaded_model = pickle.load(open(filename, 'rb'))
#         # classifier = loaded_model.score(x_test, y_test)

#         # initialise loaded_model here

#     def Predict(self,img):
#         self.img = img
#         gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
#         flat = np.ravel(gray)
#         flat = flat.T
#         flat = pca.transform(flat)
#         ID = loaded_model.predict(flat)
#         if ID == 1:
#             self.bot_ID = '0200'
#         elif ID == 2:
#             self.bot_ID = '2010'
#         elif ID == 3:
#             self.bot_ID = '0110'
#         elif ID == 4:
#             self.bot_ID = '0102'
#         return self.bot_ID 
# endregion

def orientation_line_from_angle(img,angle,cur_location):
    cX, cY = cur_location
    rad = angle*math.pi/180
    radius = 75
    dy = radius*math.sin(rad)
    dx = radius*math.cos(rad)       
    Y = int(cY - dy)
    X = int(cX + dx)
    cv2.line(img,(int(cX),int(cY)),(X,Y),(0,0,255),2)

class get_motion:
    def __init__(self,img,cur_location,cur_angle,next_point):
        self.cur_location = cur_location # current bot location
        self.cur_angle = cur_angle # current bot orientation
        self.next_point = next_point # next box location
        y = self.next_point[1] - self.cur_location[1]
        x = self.next_point[0] - self.cur_location[0]
        rad = math.atan(y,x) 
        self.seperation = math.sqrt(x**2 + y**2) # seperation between two bots
        self.req_angle =  rad*180/math.pi # bot center to next box orientation
        cv2.line(img, cur_location, next_point, (255,0,0),thickness = 3)
        # draw line form bot center to next box center

    def get_motor_vel(self):
        # anticlockwise rotation required 
        ac_rotation_req = self.req_angle - self.cur_angle 
        if ac_rotation_req > 45:
            # rotate anti clockwise for 't' time
            pass
        elif ac_rotation_req < -45:
            # rotate clockwise for 't' time
            pass
        if self.seperation < 30:
            # stop bot 
            # pop the current point
            pass
        else: 
            # move continously 
            pass
        return None#command

if __name__ == '__main__':

    # region load files
    # img = cv2.imread(f'C:/Users/OHM/Desktop/pytthon/error_imgs/66.jpg')
    cap = cv2.VideoCapture('error_imgs/v8.mp4')
    ret,frame = cap.read()
    # endregion

    # region sample bot finder
    # BF = BotFinder()
    # cv2.imshow('file',img)
    # cv2.waitKey()
    # BF.give_frame(img)
    # bot = BF.ret()
    # print(bot)
    # endregion

    # region video
    shape_identifier = ShapeIdentifier()
    BF = BotFinder()
    while True:
        ret,frame = cap.read()
        if ret is False:break 
        s= time.time()
        BF.give_frame(frame)
        bot = BF.ret()
        e = time.time()
        # print(1/(e-s))
        frame_copy = frame.copy()
        for i in bot.keys():
            # extract info from bot
            cY,cX,angle = bot[i]

            #draw circle and show bot ID  
            cv2.putText(frame_copy, str(i), (int(cX-10), int(cY)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.circle(frame_copy, (int(cX),int(cY)), 30, (0,255,255),thickness = 2)

            # draw line of orientation
            orientation_line_from_angle(frame_copy, angle, (cX,cY))

        cv2.imshow('small_frame',size_mod(frame_copy, 0.5))
        # cv2.imshow('frame',frame)
        key = cv2.waitKey(1)
        if key == 27:break
    #endregion

