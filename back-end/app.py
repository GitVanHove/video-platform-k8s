from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Dummy video storage (Replace with a database later)
videos = []

# Route to fetch all videos
@app.route("/videos", methods=["GET"])
def get_videos():
    return jsonify(videos)

# Route to upload a new video
@app.route("/upload", methods=["POST"])
def upload_video():
    data = request.json
    video_id = len(videos) + 1
    new_video = {"id": video_id, "title": data["title"], "url": data["url"]}
    videos.append(new_video)
    return jsonify({"message": "Video uploaded successfully!", "video": new_video}), 201

# Route to delete a video
@app.route("/delete/<int:video_id>", methods=["DELETE"])
def delete_video(video_id):
    global videos
    videos = [video for video in videos if video["id"] != video_id]
    return jsonify({"message": f"Video {video_id} deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)