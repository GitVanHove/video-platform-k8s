from ultralytics import YOLO
import logging
import json
import sys
import os

# Use the absolute path of AI-job folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
MODEL_PATH = os.path.join(BASE_DIR, "yolov8n.pt")  
RESULTS_FOLDER = os.path.join(BASE_DIR, "results")  

# Ensure results folder exists
os.makedirs(RESULTS_FOLDER, exist_ok=True)

print(f"Processing file: {sys.argv[1]}")

def process_video(video_path, user_id):
    model = YOLO(MODEL_PATH)
    results = model(video_path)  # Run YOLO on the video

    try:
        detections = []
        for frame in results:
            for obj in frame.boxes:
                detections.append({
                    "label": model.names[int(obj.cls)],
                    "confidence": float(obj.conf),
                    "timestamp": None  # Removed frame.idx, since it doesn't exist
                })

        # Save results inside AI-job/results
        result_path = os.path.join(RESULTS_FOLDER, f"{user_id}_{os.path.basename(video_path)}.json")
        with open(result_path, "w") as f:
            json.dump({"objects": detections}, f, indent=4)

        print(f"Results saved to {result_path}")
        logging.info("AI job completed successfully")
    except Exception as e:
        logging.error(f"Error in AI job: {e}")

if __name__ == "__main__":
    video_path = sys.argv[1]  
    user_id = sys.argv[2]  
    process_video(video_path, user_id)