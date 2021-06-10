import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from MarkAttendance import Attendance
# Helper functions
def loadFiles():
    # load data from the path
    path = "known_images_dataset/class_images"
    images = []  # to store images
    class_names = []  # to store image names as image names are classNames
    list_files = os.listdir(path)  # list of files in the directory

    for filename in list_files:
        cur_image = cv2.imread(f'{path}/{filename}')  # open images using imread
        images.append(cur_image)
        class_names.append(os.path.splitext(filename)[0])  # splits path

    return images, class_names


# Encodings of images
def encodings(images):
    encoding_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert bgr to rgb
        encode = face_recognition.face_encodings(img)[0]  # encode images
        encoding_list.append(encode)
    print("Encoding completed!!")
    return encoding_list


# mark Attendance
def mark_attendance(name):
    with open('Attendance.csv', 'r+') as f:  # open csv file
        data_list = f.readlines()   # read line by line
        names = []
        for row in data_list:
            entry = row.split(',')
            names.append(entry[0])
        if name not in names:   # notes student in time once
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            f.writelines(f'\n{name},{dt_string}')  # enter the values into csv file


# process Attendance
def capture_frame(class_names, known_encoding_list):
    cap = cv2.VideoCapture(0)  # capture video
    i = 0
    while i<10:
        success, frame = cap.read()  # read a frame
        # show original frame
        # cv2.imshow("Original", frame)
        # img_frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)  # preprocess the frame
        img_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert bgr to rgb
        # show the converted frame
        # cv2.imshow("BGR2RGB", img_frame)
        faces_cur_Location = face_recognition.face_locations(img_frame)  # find locations of faces in frame

        # encode for each and every face in the frame
        faces_cur_Encodings = face_recognition.face_encodings(img_frame, faces_cur_Location)

        for encodeFace, faceLoc in zip(faces_cur_Encodings, faces_cur_Location):
            # find the matching faces
            matches = face_recognition.compare_faces(known_encoding_list, encodeFace)
            # find least distance face in the dataset
            faceDis = face_recognition.face_distance(known_encoding_list, encodeFace)

            matchIndex = np.argmin(faceDis, axis=0)

            if faceDis[matchIndex] < 0.60:
                name = class_names[matchIndex].upper()
                mark_attendance(name)
                Attendance(name)
            else:
                name = 'Unknown'
            y1, x2, y2, x1 = faceLoc
            # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            # Display rectangle around face
            # frame2 = frame
            # cv2.rectangle(frame2, (x1, y1), (x2, y2), (51, 204, 51), 2)
            # cv2.imshow("face", frame2)
            # create a rectangle frame around the face
            cv2.rectangle(frame, (x1, y1), (x2, y2), (51, 204, 51), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (51, 204, 51), 2, cv2.FILLED)

            # insert text onto the image
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # display image
        cv2.imshow('web cam', frame)
        cv2.waitKey(1)
        i+=1


# build Model
def model():
    # using helper function to build model
    images, class_names = loadFiles()
    known_encoding_list = encodings(images)
    capture_frame(class_names, known_encoding_list)


# call model
if __name__ == '__main__':
    model()
