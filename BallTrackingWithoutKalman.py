# code without kalman filter 
import cv2
import numpy as np

cap = cv2.VideoCapture('ball_tracking_example.mp4')
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # convert the frame to HSV color space for better color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the color range for detecting the ball (tweak this based on the ball's color)
    lower_ball_color = np.array([30, 150, 50])  # Example for green ball
    upper_ball_color = np.array([85, 255, 255])

    # create a mask for ball color
    mask = cv2.inRange(hsv, lower_ball_color, upper_ball_color)

    # find contours of the masked region (the ball)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ball_position = None

    # Loop through the contours to find the ball 
    for i in contours:
        area = cv2.contourArea(i)
        if area > 500: # filter out small areas
            # Get the bounding box of the largest contour
            x, y, w , h = cv2.boundingRect(i)

            # Draw a rectangle around the ball 
            cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 2)
            # Get the center of the ball
            ball_position = (x + w // 2, y + h // 2)
            cv2.circle(frame, ball_position, 10, (255,0,0), 2) # Draw Center


    cv2.imshow('Live Ball Tracking', frame)
    cv2.waitKey(10)
