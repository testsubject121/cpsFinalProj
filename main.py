import cv2
camera = cv2.VideoCapture(1);
while(1):
    _, frame = camera.read()
    cv2.imshow('video output', frame)
    cv2.waitKey(1)
