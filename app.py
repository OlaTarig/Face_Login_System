from flask import Flask , request, render_template, jsonify
import face_recognition
import numpy as np

app=Flask(__name__)

saved_face_encoding = np.load("stored_faces/user_data.npy")


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/verify", methods=["POST"])
def verify():
   uploaded_file = request.files["image"] # Receive uploaded image
   input_image = face_recognition.load_image_file(uploaded_file) # Load the image
   input_encodings = face_recognition.face_encodings(input_image) # Get face encodings

if len(input_encodings) > 0: # Ensure a face is detected
match_result = face_recognition.compare_faces([saved_face_encoding],
input_encodings[0]) # Compare faces
if match_result[0]:
return jsonify({"Access Granted! Registered User"})
return jsonify({" Access Denied! Face not recognized"}), 401


if __name__=='__main__':
    app.run(debug=True)
