from flask import Flask, request, render_template, redirect, url_for
import numpy as np
from Authentication import recognize_image,capture_and_store_face
import cv2
from database import fetch_encoding

app = Flask(__name__)

# Load stored face encodings
encodedFaces = fetch_encoding()


@app.route('/')
def welcome():
    return render_template('welcome.html')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # Ensure the function only runs for POST requests
        capture_and_store_face()  # Capture face and store encoding
        return redirect(url_for('index'))  # Redirect to login after registration
    return render_template('register.html')
@app.route("/verify", methods=["POST"])
def verify():
    uploaded_file = request.files.get("image")
    if not uploaded_file:
        return redirect(url_for("result", status="error", message="No file uploaded"))

    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    result = recognize_image(img, encodedFaces)

    return redirect(url_for("result", status=result.lower()))
@app.route("/result")
def result():
    status = request.args.get("status", "error")  # Get status from query params
    return render_template("result.html", status=status)


if __name__ == '__main__':
    app.run(debug=True)
