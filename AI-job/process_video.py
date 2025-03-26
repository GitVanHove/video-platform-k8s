from ultralytics import YOLO
import logging
import json
import sys
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
        # Run YOLO on the video
        results = model(video_path)
        
        detections = []
        for frame_idx, frame in enumerate(results):  # Use frame_idx to keep track of frames
            for obj in frame.boxes:
                detections.append({
                    "label": model.names[int(obj.cls)],  
                    "confidence": float(obj.conf),  
                    "timestamp": frame_idx  
                })
        
        result_filename = f"{user_id}_{os.path.basename(video_path)}.json"
        result_path = os.path.join(RESULTS_FOLDER, result_filename)

        # Save the detection results to a JSON file
        with open(result_path, "w") as f:
            json.dump({"objects": detections}, f, indent=4)

        print(f"Results saved to {result_path}")
        logging.info("AI job completed successfully")

        return result_path  # Return the result path for use in the response
    
    except Exception as e:
        logging.error(f"Error in AI job: {e}")
        raise

# API endpoint to handle video uploads
@app.route('/process_video', methods=['POST'])
def handle_video():
    try:
        # Get video file and user ID from request
        video_file = request.files['video']
        user_id = request.form['user_id']
        
        # Extract the file extension and save the video file with the correct extension
        file_extension = os.path.splitext(video_file.filename)[1]  # Get the extension (e.g., .mp4, .gif, etc.)
        if file_extension.lower() not in ['.mp4', '.gif', '.avi', '.mov']:  # Add more valid formats if needed
            return jsonify({"error": "Invalid video format"}), 400
        
        video_path = os.path.join(RESULTS_FOLDER, f"{user_id}_video{file_extension}")
        video_file.save(video_path)

        # Process the video using the AI function
        result_path = process_video(video_path, user_id)

        # Return the result path to the client
        return jsonify({"message": "AI processing started successfully", "result_path": result_path}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001) 