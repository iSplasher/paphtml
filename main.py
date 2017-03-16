import cv2
import imutils
import numpy as np

img = "test2.jpg"

image = imutils.resize(cv2.imread(img), width=800) # load image
modified = image.copy()
win = cv2.namedWindow("image")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
canny = cv2.Canny(gray,60,200) # edge detection
blurred = cv2.GaussianBlur(gray, (5, 5), 0) # blur slightly to reduce noise
thresh_value = 0


def thresh_change(a):
    global thresh_value
    thresh_value = a
    draw_contour()

cv2.createTrackbar("Thresh", "image", 0, 255, thresh_change)

def draw_contour():
    global modified

    thresh = cv2.threshold(blurred, thresh_value, 255, cv2.THRESH_BINARY_INV)[1]
    modified = thresh.copy()

    # find location of white regions using contour detection
    cnt_img, cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #cv2.imshow('image', image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # loop over the contours
    for c in cnts:
        #M = cv2.moments(c)
        #cX = int((M["m10"] / M["m00"]))
        #cY = int((M["m01"] / M["m00"]))

        epsilon = 0.1*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)

        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c = c.astype("int")

        cv2.drawContours(modified, [c], 0, (0, 255, 0), 2)


    #cv2.imshow('image',gray)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #cv2.imshow('image',blurred)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #cv2.imshow('image',thresh)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #cv2.imshow('image',canny)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

while True:
    cv2.imshow('image', modified)
    if 27 == cv2.waitKey(1): # 27 is ESC
        break

cv2.destroyAllWindows()
