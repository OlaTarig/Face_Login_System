from flask import Flask, request, render_template, jsonify, redirect, url_for
import numpy as np
from Authentication import recognize_face, recognize_image
import cv2
from database import fetch_encoding

app = Flask(__name__)

# Load stored face encodings
encodedFaces = fetch_encoding()


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/verify", methods=["POST"])
def verify():
    uploaded_file = request.files.get("image")
    if not uploaded_file:
        return redirect(url_for("result", status="error", message="No file uploaded"))

    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    result = recognize_image(img, encodedFaces)

    return redirect(url_for("result", status=result.lower()))


@app.route("/verify_camera", methods=["POST"])
def verify_camera():
    result = recognize_face(encodedFaces)
    return redirect(url_for("result", status="authorized" if result else "unauthorized"))


@app.route("/result")
def result():
    status = request.args.get("status", "error")  # Get status from query params
    return render_template("result.html", status=status)


if __name__ == '__main__':
    app.run(debug=True)
