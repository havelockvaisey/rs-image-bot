import cv2 as cv
import numpy as np

def redMask(img):
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv.inRange(img_hsv, lower_red, upper_red)
    return mask1+mask0

def whiteMask(img):
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
     # mask
    lower_white = np.array([0,0,0], dtype=np.uint8)
    upper_white = np.array([0,0,255], dtype=np.uint8)

    # Threshold the HSV image to get only white colors
    mask2 = cv.inRange(img_hsv, lower_white, upper_white)
    return mask2

def yellowMask(img):
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower = np.array([22, 93, 0], dtype="uint8")
    upper = np.array([45, 255, 255], dtype="uint8")

    mask = cv.inRange(img_hsv, lower, upper)
    return mask

def grayMask(img):
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower = np.array([0, 5, 50], dtype="uint8")
    upper = np.array([179, 50, 255], dtype="uint8")

    mask = cv.inRange(img_hsv, lower, upper)
    return mask