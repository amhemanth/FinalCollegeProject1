import cv2
import face_recognition

imgStudent = face_recognition.load_image_file(r"known_images_dataset/class_images/17121A1504.jpg")
imgStudent = cv2.cvtColor(imgStudent, cv2.COLOR_BGR2RGB)

imgTest = face_recognition.load_image_file(r"test_images/imgtest1.jpg")
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

# processing known image
faceLoc = face_recognition.face_locations(imgStudent)[0]
encodeStudent = face_recognition.face_encodings(imgStudent)[0]
cv2.rectangle(imgStudent, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 255, 0), 2)

# processing test image
faceLocTest = face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 255, 0), 2)

# compare Test encoding with known encodings
result = face_recognition.compare_faces([encodeStudent], encodeTest)
# find distance between two images to know how close they are
faceDis = face_recognition.face_distance([encodeStudent], encodeTest)

print(result, faceDis)

# inserting text onto the Test image
cv2.putText(imgTest, f'{result} {round(faceDis[0], 2)}', (faceLocTest[1], faceLocTest[2]), cv2.FONT_HERSHEY_SIMPLEX, 1,
            (0, 255, 0), 2)

cv2.imshow('my image', imgStudent)
cv2.imshow('test image', imgTest)
cv2.waitKey(0)
