import numpy as np
import cv2 as cv


capture = cv.VideoCapture(2)
if not capture.isOpened:
    print('Unable to open camera')
    exit(0)
while True:
    ret, frame = capture.read()
    if frame is None:
        break
    
    # Changing the colour-space
    LUV = cv.cvtColor(frame, cv.COLOR_BGR2LUV)
    # Find edges
    edges = cv.Canny(LUV, 10, 100)
    # Find Contours
    contours, hierarchy = cv.findContours(edges,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    # Find Number of contours
    print("Number of Contours is: " + str(len(contours)))
    # Draw yellow border around two contours
    cv.drawContours(frame, contours, 0, (0, 230, 255), 6)
    cv.drawContours(frame, contours, 2, (0, 230, 255), 6)
    # Show the image with contours
    cv.imshow('Contours', frame)
    
    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break