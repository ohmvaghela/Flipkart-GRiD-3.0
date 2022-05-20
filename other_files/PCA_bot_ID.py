import cv2
from final_function import BotFinder
import time
import numpy as np
import math
from collections import deque
import matplotlib.pyplot as plt
from sklearn import decomposition
import pickle

class bot_ID:
    def __init__(self):
        self.bot_ID = ''
        loaded_model = pickle.load(open(filename, 'rb'))
        classifier = loaded_model.score(x_test, y_test)

        # initialise loaded_model here

    def Predict(self,img):
        self.img = img
        gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        flat = np.ravel(gray)
        flat = flat.T
        flat = pca.transform(flat)
        ID = loaded_model.predict(flat)
        if ID == 1:
            self.bot_ID = '0200'
        elif ID == 2:
            self.bot_ID = '2010'
        elif ID == 3:
            self.bot_ID = '0110'
        elif ID == 4:
            self.bot_ID = '0102'
        return self.bot_ID 

