import cv2
import mediapipe as mp
import pyautogui

faceMesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)
cam = cv2.VideoCapture(0)
screenWidth, screenHeight = pyautogui.size()
while True:
    _, img = cam.read()
    height, width, depth = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgProcessed = faceMesh.process(imgRGB)
    face_landmarks_points = imgProcessed.multi_face_landmarks
    # print(face_landmarks_points)
    if face_landmarks_points:
        one_face_lmPoints = face_landmarks_points[0].landmark
        for id,landmark_point in enumerate(one_face_lmPoints[474:478]):
            x = int(landmark_point.x * width)
            y = int(landmark_point.y * height)
            # print(x,y)
            if id == 1:
                mouse_x = int(screenWidth / width * x)
                mouse_y = int(screenHeight / height * y)
                pyautogui.moveTo(mouse_x, mouse_y)
            cv2.circle(img, (x,y), 2, (0,0,255))
        leftEye = [one_face_lmPoints[145], one_face_lmPoints[159]]
        for landmark_point in leftEye:
            x = int(landmark_point.x * width)
            y = int(landmark_point.y * height)
            print(x,y)
            cv2.circle(img, (x,y), 2, (0,0,255))
        if(leftEye[0].y - leftEye[1].y < 0.01):
            pyautogui.click()
            pyautogui.sleep(2)
            print('mouse clicked')
    cv2.imshow('image', img)
    key = cv2.waitKey(1)
    if key == 27:
        break
cam.release()
cv2.destroyAllWindows()