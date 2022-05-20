import cv2
from new_final_function import BotFinder
import time
import numpy as np
import threading 
from grid_maker import GridMaker
from video2 import vdo_tbar
import math
from collections import deque
import json
import datetime
import matplotlib.pyplot as plt
from Samarth_CNN.shape_identifier import ShapeIdentifier




feed = cv2.imread(f'C:/Users/OHM/Desktop/pytthon/error_imgs/{63}.jpg')
BF = BotFinder()

BF.give_frame(feed)
bot = BF.ret()

print(bot)
