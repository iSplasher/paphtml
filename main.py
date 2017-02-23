import cv2

img = "test1.jpg"

image = cv2.imread(img)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow('image',gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow('image',blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow('image',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

