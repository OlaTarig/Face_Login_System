import cv2
import numpy as np
import face_recognition
import os
from database import upload_encoding, fetch_encoding, LogAttempt

# File to track first-time launch
FLAG_FILE = "first_run.txt"

# Function to check if this is the first time launching the program
def is_first_time():
    return not os.path.exists(FLAG_FILE)

# Function to mark the program as launched
def mark_first_time():
    with open(FLAG_FILE, "w") as f:
        f.write("This program has been launched before.")

# Function to capture & store face
def capture_and_store_face():
    print("[INFO] Capturing a new face for registration...")

    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        if not success:
            print("[ERROR] Failed to capture frame from webcam.")
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
            print("[SUCCESS] Face captured and stored in the database.")
            mark_first_time()  # Mark as first-time completed
            break  # Exit loop after storing face

    cap.release()
    cv2.destroyAllWindows()

# Function to recognize face

def recognize_face(encodeListKnown):
    allow = False
    if is_first_time():
        capture_and_store_face()
    else:
        print("[INFO] First-time capture already done. Proceeding with recognition...")

    # Open webcam for face recognition
    cap = cv2.VideoCapture(0)
    encodeListKnown = np.array(encodeListKnown)  # Convert stored encodings to NumPy array

    while True:
        success, img = cap.read()
        if not success:
            print("[ERROR] Failed to capture frame from webcam.")
            break

        # Resize for faster processing & convert to RGB
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        # Detect faces and compute encodings
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            status = ""
            if len(faceDis) > 0:
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    status = "Authorized"
                    allow = True
                    color = (0, 255, 0)  # Green
                    print("[INFO] Authorized person detected. Stopping webcam...")

                    # Convert face coordinates to original size
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                    # Draw rectangle around face
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), color, cv2.FILLED)
                    cv2.putText(img, status, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                    # Log Attempt
                    #LogAttempt(status)

                    # Display result for a brief moment and stop
                    cv2.imshow('Webcam', img)
                    cv2.waitKey(2000)  # Show the result for 2 seconds
                    cap.release()
                    cv2.destroyAllWindows()
                    return  # Exit function once an authorized face is detected

        # Show webcam feed continuously until a match is found
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Allow manual exit
            break

    cap.release()
    cv2.destroyAllWindows()
    return allow

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
            return "Authorized person detected"
        else:
            return "Unauthorized person detected"
def main():
    recognize_face()

if __name__ == "__main__":
    main()
