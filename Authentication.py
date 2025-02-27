import cv2
import numpy as np
import face_recognition
import os
from database import upload_encoding, LogAttempt

def load_images(path):
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        processed_img = process_image(curImg)
        upload_encoding(processed_img)

def process_image(img):
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect faces and compute encodings
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    return encodesCurFrame[0].tobytes()

def capture_and_store_face():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        if not success:
            return "Failure"
            break

        # Resize for faster processing
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        # Detect face and compute encoding
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        if encodesCurFrame:
            encoding_blob = encodesCurFrame[0].tobytes()
            upload_encoding(encoding_blob)
             # Mark as first-time completed
            break  # Exit loop after storing face

    cap.release()
    cv2.destroyAllWindows()

# Function to recognize face
def recognize_image(img,encodeListKnown):
    processedImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encodeListKnown = np.array(encodeListKnown)
    imgFrame = face_recognition.face_locations(processedImage)
    encodedImage = face_recognition.face_encodings(processedImage,imgFrame)
    encodedImage = np.array(encodedImage[0])
    matches = face_recognition.compare_faces(encodeListKnown,encodedImage)
    faceDis = face_recognition.face_distance(encodeListKnown, encodedImage)
    if len(faceDis) > 0:
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            LogAttempt("Authorized")
            return "Authorized"
        else:
            LogAttempt("Unauthorized")
            return "Unauthorized"
def main():
    load_images("ImageAttendance")

if __name__ == "__main__":
    main()