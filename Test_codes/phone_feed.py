

# Using Android IP Webcam video .jpg stream (tested) in Python2 OpenCV3

import urllib3
import cv2
import numpy as np
import time
# Replace the URL with your own IPwebcam shot.jpg IP:port
url='http://192.168.29.215.8080/shot.jpg'


while True:
    # Use urllib to get the image from the IP camera
    imgResp = urllib3.request.urlopen(url)
    urllib3.request.
    urllib3.l
    # Numpy to convert into a array
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    
    # Finally decode the array to OpenCV usable format ;) 
    img = cv2.imdecode(imgNp,-1)
	
	
	# put the image on screen
    cv2.imshow('IPWebcam',img)

    #To give the processor some less stress
    #time.sleep(0.1) 

    # Quit if q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




