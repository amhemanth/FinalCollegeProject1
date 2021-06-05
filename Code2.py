import os
import math
import time
import cv2 as cv 
import numpy as np
from time import sleep

# Reducing the weights of the original frame 
# to compute fast with out effecting quality.

width = 480  
height = 340 

# haar face detector is used.
face_detector_kind = 'haar'

# Diagonal and line thickness are computed at run-time
diagonal, line_thickness = None, None  

# Initialize numpy random generator
np.random.seed(int(time.time()))

# Create a video capture object to read Camera video
cap = cv.VideoCapture(0) 
face_cascade = cv.CascadeClassifier('face_haar/haarcascade_frontalface_alt.xml')

# Helper functions 
def calculateParameters(height_orig, width_orig):
    global width, height, diagonal, line_thickness
    area = width * height
    width = int(math.sqrt(area * width_orig / height_orig))
    height = int(math.sqrt(area * height_orig / width_orig))
    # Calculate diagonal 
    diagonal = math.sqrt(height * height + width * width)
    # Calculate line thickness to draw boxes
    line_thickness = max(1, int(diagonal / 150))
    # Initialize output video writer
    global out 
    fps = cap.get(cv.CAP_PROP_FPS)
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter('video.avi', fourcc=fourcc, fps=fps, frameSize=(width, height))

def findFaces(img, confidence_threshold=0.7):
    # Get original width and height
    height = img.shape[0]
    width = img.shape[1]

    face_boxes = []

    # Get grayscale image
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Detect faces
    # Todo: Check the minNeighbors what happens if we change?
    detections = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors = 5)

    # Todo: Check face padding ratio
    face_padding_ratio = 0.1

    for (x, y, w, h) in detections:
        padding_h = int(math.floor(0.5 + h * face_padding_ratio))
        padding_w = int(math.floor(0.5 + w * face_padding_ratio))

        x1, y1 = max(0, x - padding_w), max(0, y - padding_h)
        x2, y2 = min(x + w + padding_w, width -1), min(y + h + padding_h, height - 1)
        face_boxes.append([x1, y1, x2, y2])

    return face_boxes

def collectFaces(frame, face_boxes):
    faces = []
    # Process faces
    for i, box in enumerate(face_boxes):
        # Convert box coordinates from resized frame_bgr back to original frame
        box_orig = [
            int(round(box[0] * width_orig / width)),
            int(round(box[1] * height_orig / height)),
            int(round(box[2] * width_orig) / width),
            int(round(box[3] * height_orig) / height),
        ]
        # Extract face box from original frame
        face_bgr = frame[
            max(0, box_orig[1]):min(box_orig[3] +1, height_orig - 1),
            max(0, box_orig[0]):min(box_orig[2] + 1, width_orig -1),
            :
        ]
        faces.append(face_bgr)
    return faces

# Process Video
paused = False
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break   

    # Calculate parameters if not yet
    if(diagonal is None):
        height_orig, width_orig = frame.shape[0:2]
        calculateParameters(height_orig, width_orig)

    # Resize, Convert BGR to HSV
    if((height, width) != frame.shape[0:2]):
        frame_bgr = cv.resize(frame, dsize=(width, height), fx=0, fy=0)
    else:
        frame_bgr = frame
    
    # Detect faces
    face_boxes = findFaces(frame_bgr)

    # Make a copy of original image
    faces_bgr = frame_bgr.copy()
    if(len(face_boxes) > 0):
        # Draw boxes in faces_bgr image
        for(x1, y1, x2, y2) in face_boxes:
            cv.rectangle(faces_bgr, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=line_thickness, lineType=8)
        
        # Collect all faces into matrix
        faces = collectFaces(frame, face_boxes)

        # Todo: Labels = face detection function
        labels = None
        # Todo : Write text on to the cv 

    # show frames
    cv.imshow('Source', frame_bgr)
    cv.imshow('Faces', faces_bgr)

    # Write ouput frame
    out.write(faces_bgr)

    # Ouit on ESC button, pause on SPACE
    key = (cv.waitKey(1 if (not paused) else 0) & 0xFF)
    if(key == 27):
        break
    elif(key == 32):
        paused = (not paused)
    sleep(0.001)

cap.release()
out.release()
cv.destroyAllWindows()