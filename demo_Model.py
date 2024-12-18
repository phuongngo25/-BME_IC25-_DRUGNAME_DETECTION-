from ultralytics import YOLO
from IPython.display import display, Image

model = YOLO("yolo11n.pt")
model = YOLO("E:/BME_INNOVATION-_PREDIX/runs/detect/train6/weights/best.pt")
# results = model.train(data ="E:/BME_INNOVATION-_PREDIX/drugOD/data.yaml", task ='detect',epochs = 3 )

# results 

#Testing 

results = model.predict("E:/BME_INNOVATION-_PREDIX/drugOD/test/download (4).jpg") #E:\BME_INNOVATION-_PREDIX\drugOD\test\download (4).jpg
results