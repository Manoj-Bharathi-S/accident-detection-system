import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Ensure required directories exist
os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "data", "input"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "data", "output"), exist_ok=True)

# Video Input
default_video_path = os.path.join(BASE_DIR, "data", "input", "sample1_720.mp4")
VIDEO_SOURCE = os.getenv("VIDEO_SOURCE", default_video_path)

# Detection Settings
YOLO_MODEL = os.getenv("YOLO_MODEL", "yolov8n.pt")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))

# Alert Settings
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "test@example.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "police@example.com")

MAILTRAP_TOKEN = os.getenv("MAILTRAP_TOKEN", "")

# Analysis Settings
# Speed threshold to be considered "high speed" (arbitrary unit, e.g., pixels/frame)
HIGH_SPEED_THRESHOLD = float(os.getenv("HIGH_SPEED_THRESHOLD", 20.0))
# Number of consecutive frames bounding boxes must overlap to be considered a collision
COLLISION_FRAME_OVERLAP = int(os.getenv("COLLISION_FRAME_OVERLAP", 5))

# Logging
default_log_path = os.path.join(BASE_DIR, "logs", "accidents.csv")
LOG_FILE = os.getenv("LOG_FILE", default_log_path)
