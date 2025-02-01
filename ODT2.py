import cv2
import urllib.request
import numpy as np
from ultralytics import YOLO  # type: ignore # YOLOv8 for training & detection

# Load YOLOv8 model (Pretrained or Custom)
model = YOLO("yolov8n.pt")  # Pretrained YOLOv8 model (use "yolov8n.pt" for quick results)

# Define ESP32-CAM URL
url = 'http://192.168.1.17/cam-hi.jpg'

# Function to train YOLOv8 on labeled dataset
def train_model():
    model = YOLO("yolov8n.yaml")  # Use YOLOv8 nano for training
    model.train(data="data.yaml", epochs=50, imgsz=640)  # Train on labeled data

# Function to detect objects from ESP32-CAM
def detect_objects():
    cv2.namedWindow("ESP32-CAM Object Detection", cv2.WINDOW_AUTOSIZE)
    
    while True:
        try:
            # Fetch image from ESP32-CAM
            img_resp = urllib.request.urlopen(url)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            im = cv2.imdecode(imgnp, -1)

            # Run YOLOv8 detection
            results = model(im)
            im = results[0].plot()  # Draw bounding boxes
            
            # Display output
            cv2.imshow('ESP32-CAM Object Detection', im)

            key = cv2.waitKey(5)
            if key == ord('q'):  # Press 'q' to exit
                break

        except Exception as e:
            print(f"Error: {e}")

    cv2.destroyAllWindows()

# Train model (Uncomment to train)
# train_model()

# Run object detection
detect_objects()
