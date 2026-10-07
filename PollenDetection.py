import cv2 as cv
import numpy as np
import time
start = time.perf_counter()
timee = 0

#replace "path" w/ image

def findCircles(img):

    circles = cv.HoughCircles(
                            img,
                            cv.HOUGH_GRADIENT,
                            dp = 1,
                            minDist = 50,
                            param1 = 64,
                            param2 = 20,
                            minRadius = 20,
                            maxRadius = 500
                              )
    return circles

    #looks for circles in img (mask in this case) that fit specifications

# I gave up and now I'm just going to manually remove any circle that fully fits in another
def filterInner(circles):
    if len(circles[0, :]) <= 1:
            return circles
    newCircles = []
    for c1 in circles[0, :]:
        x1, y1, r1 = c1[0] , c1[1], c1[2]
        for c2 in circles[0, :]:
            x2, y2, r2 = c2[0] , c2[1], c2[2]

            d = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            if(d > r1):
                newCircles.append(c2)
            elif ((d + r2) > r1):
                newCircles.append(c2)
    newCircles = np.array(newCircles, dtype=np.float32).reshape(1, -1, 3)
    return newCircles

def transform(mask):
    kernal = np.ones((8,8), np.uint8)
    closingKernal = cv.getStructuringElement(cv.MORPH_RECT, (25, 25))
    k_size = 31
    mask = cv.erode(mask, kernal, iterations = 1)
    
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, closingKernal)
    mask = cv.medianBlur(mask, 5, 2)
    mask = cv.GaussianBlur(mask, (k_size,k_size), 1)
    return mask

    #changes mask to better detect pollen

#the part where it does the stuff
def runPipeline(image, llrobot):
    timee = time.perf_counter()
    #timee bc you can't name a variable "time"
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)


    yellow_upper = np.array([40, 255, 255])
    yellow_lower = np.array([5, 30, 40])


    mask = cv.inRange(hsv, yellow_lower, yellow_upper)

    mask = transform(mask)
    circles = findCircles(mask)





    if circles is not None:
        circles = filterInner(circles)
        circles = np.uint16(np.around(circles))
        print(circles)
        for c in circles[0, :]:
            print(c)
            x, y, r = c[0] , c[1], c[2]
            cv.circle(image, (x, y), r, (0, 255, 0), 2)  # Circle outline
            cv.circle(image, (x, y), 2, (0, 0, 255), 3)  # Center point

    return [], image, llrobot
    #shows image


