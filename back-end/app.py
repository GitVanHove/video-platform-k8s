from flask import Flask, request, jsonify, send_from_directory
import subprocess
import sqlite3
import bcrypt
import os
import sys

from utils import wait_for_file 

app = Flask(__name__)
DATABASE = "users.db"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Function to connect to database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB with pre-defined users
def init_db():
    users = [
        {"username": "admin", "password": "admin123"},
        {"username": "user1", "password": "password1"},
        {"username": "user2", "password": "password2"}
    ]

    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        for user in users:
            hashed_pw = bcrypt.hashpw(user["password"].encode('utf-8'), bcrypt.gensalt())
            try:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user["username"], hashed_pw))
            except sqlite3.IntegrityError:
                pass 

        conn.commit()
    print("Database initialized with hardcoded users")

# login route
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password").encode('utf-8')

    with get_db() as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and bcrypt.checkpw(password, user["password"]):
            return jsonify({"message": "Login successful", "user_id": user["id"]})
        return jsonify({"error": "Invalid credentials"}), 401

#  Upload Video
@app.route("/upload/<int:user_id>", methods=["POST"])
def upload_video(user_id):
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files["video"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    user_folder = os.path.join(app.config["UPLOAD_FOLDER"], str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    file_path = os.path.join(user_folder, file.filename)
    file.save(file_path)

    if not wait_for_file(file_path):
        return jsonify({"error": "File was not fully saved!"}), 500

    absolute_file_path = os.path.abspath(file_path)

    print(f"Starting AI job for: {absolute_file_path}")  # Debugging line

    try:
        subprocess.Popen(["python", "../AI-job/process_video.py", absolute_file_path, str(user_id)], 
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Error starting AI job: {e}")
        return jsonify({"error": "Failed to start AI processing"}), 500

    return jsonify({"message": "Video uploaded successfully, AI processing started!"})

# All Videos for User
@app.route("/videos/<int:user_id>", methods=["GET"])
def get_user_videos(user_id):
    user_folder = os.path.join(UPLOAD_FOLDER, str(user_id))
    if not os.path.exists(user_folder):
        return jsonify({"videos": []})  # Return empty list if no videos

    videos = os.listdir(user_folder)
    return jsonify({"videos": videos})

# Detail Page
@app.route("/video/<int:user_id>/<string:filename>", methods=["GET"])
def get_video(user_id, filename):
    user_folder = os.path.join(UPLOAD_FOLDER, str(user_id))
    if not os.path.exists(os.path.join(user_folder, filename)):
        return jsonify({"error": "Video not found"}), 404

    return send_from_directory(user_folder, filename)

# Delete Video
@app.route("/video/<int:user_id>/<string:filename>", methods=["DELETE"])
def delete_video(user_id, filename):
    user_folder = os.path.join(UPLOAD_FOLDER, str(user_id))
    file_path = os.path.join(user_folder, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "Video not found"}), 404

    os.remove(file_path)
    return jsonify({"message": "Video deleted successfully"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)    