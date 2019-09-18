import cv2
import numpy as np

image = cv2.imread('test_image.jpg') # cv2 helps us to read the image as a matrix
lane_image = np.copy(image)
gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY) # we need to convert our image to RGB2GRAY because int this way, it is faster and more accurate to process the edges.
blur = cv2.GaussianBlur(gray, (5,5), 0) # this is optional since, canny() function already makes a 5,5 Gaussian when we call it.
canny = cv2.Canny(blur, 50, 150) # canny function detects edges by taking derivatives on the x and y axis and decides whether a pixel is an edge or not.
cv2.imshow('result', canny)
cv2.waitKey(0)
