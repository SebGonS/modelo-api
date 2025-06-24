from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
from supabase_utils import send_to_supabase
from PIL import Image
import io

# Optional: from supabase_utils import send_to_supabase

app = FastAPI()
model = YOLO("yolov8_multimodal.pt")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    results = model(image)

    detections = []
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        cls_name = model.names[cls_id]

        detection = {
            "class": cls_name,
            "confidence": conf,
            "bbox": [x1, y1, x2, y2]
        }

        send_to_supabase(detection)
        detections.append(detection)

    return {"detections": detections}
