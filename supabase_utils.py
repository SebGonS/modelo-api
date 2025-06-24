import requests
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def send_to_supabase(detection):
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[Supabase] Missing credentials. Skipping insert.")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "detection_id": detection["detection_id"], 
        "class": detection["class"],
        "confidence": detection["confidence"],
        "bbox_x1": detection["bbox_x1"],
        "bbox_y1": detection["bbox_y1"],
        "bbox_x2": detection["bbox_x2"],
        "bbox_y2": detection["bbox_y2"],
        "source_image": detection.get("source_image", "uploaded")
    }

    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/detections",
            json=payload,
            headers=headers
        )

        if response.status_code == 201:
            print("[Supabase] ✅ Detection logged")
        else:
            print(f"[Supabase] ❌ Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"[Supabase] ❌ Exception: {e}")
