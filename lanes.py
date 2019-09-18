import cv2
import numpy as np

#transforms the parameter image to gray (easy to process) and makes it an 5,5 gaussian blurred.
def canny(image):
    gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5, 5), 0)
    canny = cv2.Canny(blur,50, 150) # Canny function detects edges by taking derivatives on the x and y axis and decides whether a pixel is an edge or not.
    return canny


#masking the region of interest.
def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image



image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)
canny = canny(lane_image)
cropped_image = region_of_interest(canny)
cv2.imshow('result', cropped_image)
cv2.waitKey(0)
