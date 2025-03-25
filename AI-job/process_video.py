from ultralytics import YOLO
import json
import sys
import os

MODEL_PATH = "yolov8n.pt" 
RESULTS_FOLDER = "results"

# Ensure results folder exists
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def process_video(video_path, user_id):
    model = YOLO(MODEL_PATH)
    results = model(video_path)  # Run YOLO on the video

    detections = []
    for frame in results:
        for obj in frame.boxes:
            detections.append({
                "label": model.names[int(obj.cls)],
                "confidence": float(obj.conf),
                "timestamp": frame.idx  
            })

    # Save results in JSON
    result_path = os.path.join(RESULTS_FOLDER, f"{user_id}_{os.path.basename(video_path)}.json")
    with open(result_path, "w") as f:
        json.dump({"objects": detections}, f, indent=4)

    print(f"Results saved to {result_path}")

if __name__ == "__main__":
    video_path = sys.argv[1]  
    user_id = sys.argv[2]  
    process_video(video_path, user_id)