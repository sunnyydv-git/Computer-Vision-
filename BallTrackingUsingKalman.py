# code with kalman filter 
import cv2
import numpy as np

cap = cv2.VideoCapture('ball_tracking_example.mp4')

# Define the kalman filter paramters 
kalman = cv2.KalmanFilter(4,2)  # 4 -> Dynamic, 2 -> measurement
kalman.measurementMatrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0]], np.float32)
kalman.transitionMatrix = np.array([[1, 0, 1, 0],
                                    [0, 1, 0, 1],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]], np.float32)
kalman.processNoiseCov = np.array([[1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1]], np.float32) * 0.03

# variables to hold the previous ball position for speed calculation
prev_ball_position = None
prev_time = None


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

            # measure the ball position for kalman filter 
            measured = np.array([[np.float32(ball_position[0])], [np.float32(ball_position[1])]])

            # correct the kalman filter based on the current measure position
            kalman.correct(measured)
            
            # predict the next position of the ball using kalman filter
            prediction = kalman.predict()

            # Draw the predicted position
            cv2.circle(frame, (int(prediction[0]), int(prediction[1])), 10, (0,0,255), 2)

            # Estimate the ball speed if previous position is available
            if prev_ball_position is not None:
                time_elapsed = cv2.getTickCount() - prev_time
                time_elapsed /= cv2.getTickFrequency()  # Convert to seconds
                speed = np.linalg.norm(np.array(ball_position) - np.array(prev_ball_position)) / time_elapsed
                cv2.putText(frame, f"Speed: {speed:.2f} px/s", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0),2)

            # update previous ball position and time 
            prev_ball_position = ball_position
            prev_time = cv2.getTickCount()




    cv2.imshow('Live Ball Tracking', frame)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# release resources 
cap.release()
cv2.destroyAllWindows()
