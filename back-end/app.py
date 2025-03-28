from flask import Flask, request, jsonify, send_from_directory
import requests
import sqlite3
import bcrypt
import os
import uuid
import random


from utils import wait_for_file 

app = Flask(__name__)
DATABASE = "users.db"

UPLOAD_FOLDER = "uploads"
RESULTS_FOLDER = "results"  
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULTS_FOLDER"] = RESULTS_FOLDER
ALLOWED_EXTENSIONS = {'.mp4', '.gif', '.avi', '.mov'}


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

# Helper: Generate unique filename with correct extension
def generate_unique_filename(user_id, original_filename):
    file_extension = os.path.splitext(original_filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return None  
    unique_id = uuid.uuid4().hex[:8]  
    return f"{user_id}_{unique_id}{file_extension}"

# Upload Video
@app.route("/upload/<int:user_id>", methods=["POST"])
def upload_video(user_id):
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files["video"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    unique_filename = generate_unique_filename(user_id, file.filename)
    if not unique_filename:
        return jsonify({"error": "Invalid file format"}), 400

    user_folder = os.path.join(UPLOAD_FOLDER, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    
    video_path = os.path.join(user_folder, unique_filename)
    file.save(video_path)

    if not os.path.exists(video_path):
        return jsonify({"error": "File was not fully saved!"}), 500

    absolute_file_path = os.path.abspath(video_path)

    try:
        ai_service_url = 'http://ai-job:5001/process_video'

        with open(video_path, 'rb') as video_file:
            files = {'video': video_file}
            data = {'user_id': user_id}
            response = requests.post(ai_service_url, files=files, data=data)

        if response.status_code == 200:
            return jsonify({
                "message": "AI processing started successfully",
                "video_filename": unique_filename
            }), 200
        else:
            return jsonify({
                "error": f"Failed to start AI processing: {response.text}"
            }), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"AI service request failed: {str(e)}"}), 500


# All Videos for User
@app.route("/videos/<int:user_id>", methods=["GET"])
def get_user_videos(user_id):
    user_folder = os.path.join(UPLOAD_FOLDER, str(user_id))
    if not os.path.exists(user_folder):
        return jsonify({"videos": []}) 

    videos = os.listdir(user_folder)
    return jsonify({"videos": videos})

# Detail Page
@app.route("/detail/<int:user_id>/<string:video_filename>", methods=["GET"])
def get_video_and_json(user_id, video_filename):
   
    user_folder = os.path.join(UPLOAD_FOLDER, str(user_id))
    
    json_filename = video_filename.replace(".mp4", ".json").replace(".gif", ".json")
    json_path = os.path.join(RESULTS_FOLDER, json_filename)

    video_path = os.path.join(user_folder, video_filename)

    if not os.path.exists(video_path):
        return jsonify({"error": "Video not found"}), 404

    if not os.path.exists(json_path):
        return jsonify({"error": "JSON file not found"}), 404

    video_url = f"http://127.0.0.1:5000/video/{user_id}/{video_filename}"
    json_url = f"http://127.0.0.1:5000/json/{json_filename}"

    return jsonify({
        "video_url": video_url,
        "json_url": json_url
    }), 200

# Serve the video file from the uploads folder
@app.route("/video/<int:user_id>/<string:video_filename>", methods=["GET"])
def get_video(user_id, video_filename):
    user_folder = os.path.join(UPLOAD_FOLDER, str(user_id))
    return send_from_directory(user_folder, video_filename)

# Serve the JSON file from the results folder
@app.route("/json/<string:json_filename>", methods=["GET"])
def get_json(json_filename):
    return send_from_directory(RESULTS_FOLDER, json_filename)


# Delete Video
@app.route("/video/<int:user_id>/<string:video_filename>", methods=["DELETE"])
def delete_video(user_id, video_filename):
    user_folder = os.path.join(UPLOAD_FOLDER, str(user_id))
    video_path = os.path.join(user_folder, video_filename)
    
    base_filename = os.path.splitext(video_filename)[0] 
    json_filename = f"{base_filename}.json"
    json_path = os.path.join(RESULTS_FOLDER, json_filename)

    if os.path.exists(video_path):
        os.remove(video_path)
    else:
        return jsonify({"error": "Video not found"}), 404

    if os.path.exists(json_path):
        os.remove(json_path)
    else:
        return jsonify({"error": "JSON results not found"}), 404

    return jsonify({"message": "Video and associated results deleted successfully"}), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000,debug=True)    