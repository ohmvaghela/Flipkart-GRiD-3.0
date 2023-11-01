# Flipkart GRiD 3.0

- Functions

| Function | Defination   | Input |
| -------- | ------------ |-|
| size_mod | Resize Image | image , times|
| orientation_line_from_angle | Draw Line | image, angle, center_coorinates| 
| min_dist | Euler Distance | coordiante_1, coordiante_2 |
|img_align | Prespective Transfromation of image from points (a,b,c,d) to (a1,b1,c1,d1)  vertex of rectangle (Goto end for code) | image, inital points (a,b,c,d), final size of image height and width |

## Classes

### Angle

| Function | Defination   | Input |
| -------- | ------------ |-|
| init | Resize Image | image , times|
| orientation_line_from_angle | Draw Line | image, angle, center_coorinates| 
| min_dist | Euler Distance | coordiante_1, coordiante_2 |

### BotFinder
- Variables
    | Varable | Defination |
    |- | -|
    |bot_ID_all|list of all bot_id available|
    |init1,init2|Pickup points|


>#### imageAlign
> ```python
>   def img_align(img,pts,size_x,size_y):
>       img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
>       rows,cols,ch = img_gray.shape
>       pts1 = np.float32(pts)
>       pts2 = np.float32([[0,0],[size_x,0],[size_x,size_y],[0,size_y]])
>       # Get transform matrix 
>       M = cv2.getPerspectiveTransform(pts1,pts2)
>       # Crop matrix, multiply matrix, resize matrix
>       dst = cv2.warpPerspective(img,M,(size_x,size_y))
>       return dst
> ```

### ExtractContour

- Convert to HSV
- purple mask
- Morphologial Open
- Blue
- Morph Erode



### Morphological Operation
- GreyScale 
    - Black - 0
    - White - 1
- Erode
    - White boundries to black
- Dilate
    - Black boundries to White
- Open : Remove noise
    - Erode and Dilate
- Close : Close hole
    - Dilate and Erode
- Gradient
    - Dilate - Erode
    

### Canny Edge

- Based on Sobel Edge detector
    - In sobel edge each pixel is multiplied with a matrix like
    
        ||||
        |-|-|-|
        |-1|0|1|
        |-2|0|2|
        |-1|0|1|
    - So for each pixel if on its left and right intensities are differnt so this will result a non zero value
    - This is for vectical edge detection
    - Same goes for horizontal edge detecton
    - Say for a point from vertical edge we get a value and name it gradient_x (Gx) and for horizontal say gradient_y (Gy)
    - So for each pixel we have gradient as sqrt(Gx^2 + Gy^2) 
    - Now this output gradient is scaled to 0 to 255 on greyscale

- Canny Edge
    - It is based on sobel operator's output we have edge with it's direction 
    - based on direction we can check the neighbor and find the max value and eleminate others
    - in the image shown when comparing w.r.t to blue line yellow line will be eleminated or coverted to black
    <center>

    <img src='./canny_edge.png' width="500"/>

    </center>
    - Now we have boundary of image as pixel intensitied from 0 to 255
    - So if we have a line in an image with pixel intensity on y-axis so we can perform hystresis thresolding
    - So we pick upper bound and lower bound
    - All the intensities over upper bound are reserved 
    - All the intensities between lower and upper bound are stored if are connected with upper bound 
    - And All below lower bound are discarded
    
    <center>

    <img src='./thresh.png' width="500"/>

    </center>
