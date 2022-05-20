import numpy as np
import cv2
from pyzbar.pyzbar import decode


frame = cv2.imread(f'C:/Users/OHM/Desktop/barcodeimg.png')
detectedBarcodes = decode(frame)
print(detectedBarcodes)
for barcode in detectedBarcodes:
     
    (x, y, w, h) = barcode.rect
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
  
    print(barcode.data)
    print(barcode.type)
 
 
cv2.imshow("frame", frame)
  
cv2.waitKey(0)
cv2.destroyAllWindows()