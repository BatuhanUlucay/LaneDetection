import cv2
import numpy as np

#transforms the parameter image to gray (easy to process) and makes it an 5,5 gaussian blurred.
def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5, 5), 0)
    canny = cv2.Canny(blur,50, 150) # Canny function detects edges by taking derivatives on the x and y axis and decides whether a pixel is an edge or not.
    return canny


#masking the region of interest.
def region_of_interest(image):
    height = image.shape[0]
    width = image.shape[1]

    mask = np.zeros_like(image)

    polygons = np.array([
    [(200, height), (550, 250), (1100, height)]
    ], np.int32)

    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

#iterating through the lines and take them as 2D array, returns blue lines.
def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        for x1, y1, x2, y2 in line:

            #x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1,x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]

            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope,intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    averaged_lines = [left_line, right_line]
    return averaged_lines



def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*3/5)
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return [[x1, y1, x2, y2]]


image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)
canny_image = canny(lane_image)
cropped_image = region_of_interest(canny_image)

# here is the magic, the following line makes a Hough Space of the points and votes for every intersection, decides for the lines.
lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
averaged_lines = average_slope_intercept(image, lines)
line_image = display_lines(lane_image, averaged_lines)
combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 0)
cv2.imshow('result', combo_image)
cv2.waitKey(0)
