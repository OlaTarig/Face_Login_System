# Face_Login_System
The Face Recognition for Smart Homes project provides a secure and convenient login system using facial recognition.
It uses Flask to create an API that handles user face registration, storage, and authentication.
# Features
✅ Secure Face Authentication – Uses biometric recognition instead of passwords.

✅ Fast and Efficient – Real-time face detection and login authentication.

✅ Flask API Integration – Backend API for processing login requests.

✅ SQLite Database – Stores registered user face data.

✅ User-Friendly Interface – Simple and interactive frontend.
# 🛠️ Technologies Used
🐍 Python & NumPy – Core programming and data processing.

🎭 OpenCV – For face detection and processing.

🆔 Face Recognition Library – To authenticate users.

🌐 Flask – For backend API development.

🗄️ SQLite – To store user data.
# 📂 Project Structure
📦 Face_Login_System

 ┣ 📂 static/            # Frontend assets (CSS, JS, images)
 
 ┣ 📂 templates/         # HTML files for UI
 
 ┣ 📜 main.py            # Main Flask application
 
 ┣ 📜 Authentication.py  # Face detection and recognition logic
 
 ┣ 📜 database.db        # SQLite database for storing user data
 
 ┣ 📜 requirements.txt   # Required dependencies
 
 ┗ 📜 README.md          # Project documentation
 
# 🔧 Installation & Setup

1️⃣ Clone the repository
git clone https://github.com/OlaTarig/Face_Login_System.git 
cd Face_Login_System

2️⃣ Create a virtual environment & activate it
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\\Scripts\\activate   # On Windows\

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Flask app
python main.py

5️⃣ Access the application
Open your browser and go to:
http://127.0.0.1:5000/

# 🎯 How It Works?

1️⃣ User Registration – Face images are captured and stored in the database.

2️⃣ Login Attempt – The system detects a face when a user tries to log in.

3️⃣ Face Matching – Compares the detected face with stored data.

4️⃣ Authentication Result – Grants access if a match is found; otherwise, denies login.

# 🏆 Challenges Faced

⚡ Handling variations in lighting conditions affecting face recognition.

⚡ Ensuring high accuracy while reducing false positives.

⚡ Securing the backend API from unauthorized access.

# 🚀 Future Improvements
🔹 Implement multi-user support with different access levels.

🔹 Add encryption for better security.

# 💡 Contribution & Feedback

We welcome contributions! Feel free to fork the repo, create a new branch, and submit a pull request.
For any questions, open an issue or reach out to us!

# ✅ Project by:
Ola Tarig

Rayoof Alrashoud







