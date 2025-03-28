from ultralytics import YOLO
import logging
import json
import os
from flask import Flask, request, jsonify

# Define paths
MODEL_PATH = "models/yolov8n.pt"
RESULTS_FOLDER = "/app/results"
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app = Flask(__name__)

model = YOLO(MODEL_PATH)

# AI processing function
def process_video(video_path, user_id):
    try:
        results = model(video_path)

        detections = []
        for frame_idx, frame in enumerate(results):  # Use frame_idx to keep track of frames
            for obj in frame.boxes:
                detections.append({
                    "label": model.names[int(obj.cls)],
                    "confidence": float(obj.conf),
                    "timestamp": frame_idx
                })

        # FIX: Ensure filename matches video (without .mp4 extension)
        base_filename = os.path.splitext(os.path.basename(video_path))[0]  
        result_filename = f"{base_filename}.json"
        result_path = os.path.join(RESULTS_FOLDER, result_filename)

        with open(result_path, "w") as f:
            json.dump({"objects": detections}, f, indent=4)

        print(f"Results saved to {result_path}")
        logging.info("AI job completed successfully")

        return result_path  

    except Exception as e:
        logging.error(f"Error in AI job: {e}")
        raise

@app.route('/process_video', methods=['POST'])
def handle_video():
    try:
        # Ensure video is uploaded
        if 'video' not in request.files:
            return jsonify({"error": "No video file provided"}), 400

        video_file = request.files['video']
        user_id = request.form['user_id']

        # Save the uploaded video temporarily
        temp_video_path = os.path.join("/tmp", video_file.filename)
        video_file.save(temp_video_path)

        # Process the video
        result_path = process_video(temp_video_path, user_id)

        # Remove the temporary file after processing
        os.remove(temp_video_path)

        return jsonify({
            "message": "AI processing completed successfully",
            "result_path": result_path
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# Start the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001) 