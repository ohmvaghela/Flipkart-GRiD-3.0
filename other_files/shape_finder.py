import cv2
for i in range(4000):

    try:    
        path = f'C:/Users/OHM/Desktop/pytthon/2010/{i}.png'
        

        temp = cv2.imread(path)
        temp = cv2.resize(temp, (100,100))
        cv2.imwrite(path, temp)
        print(i)
    except:pass
