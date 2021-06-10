import cv2
cap = cv2.VideoCapture(0)
while True:
    success, frame = cap.read()
    cv2.imshow("input", frame)
    img_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("BGR2RGB", img_frame)