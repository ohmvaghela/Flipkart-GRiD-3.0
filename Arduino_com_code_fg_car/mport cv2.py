import cv2
import numpy as np

cap = cv2.VideoCapture(1)

cap.set(3, 1920)
cap.set(4, 1080)

def size_mod(img,times):
    h,w = img.shape[:2]
    dim = (int(w*times), int(h*times))
    return cv2.resize(img, dim)

while(True):
    ret, frame = cap.read()
    frame = size_mod(frame,0.5)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()