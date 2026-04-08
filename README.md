# AI-Based Real-Time Road Accident Detection System

This application is a real-time, computer vision-powered system designed to process live CCTV or sample dashcam video feeds to detect road accidents. It utilizes **YOLOv8** for robust vehicle detection and applies algorithmic models to track relative velocity and bounding-box overlap, allowing it to infer collision severity and potential causes (like sudden braking).

In the event of a high-severity collision, the system automatically logs the incident to a CSV file and can dispatch an immediate SMTP email alert to emergency services, detailing the Google Maps coordinates. Once execution concludes, a Matplotlib-powered dashboard visualizes accident trends.

## Core Features
1. **Real-Time Tracking**: Fast, frame-by-frame inference powered by Ultralytics YOLOv8.
2. **Accident Analysis**: Detects collisions exclusively based on tracked bounding boxes intersecting for a set threshold.
3. **Emergency Alerting**: Instant SMTP warning loop for targeted contacts.
4. **Analytics Engine**: Uses Pandas and Matplotlib to analyze stored `logs/` to yield accident causation pie charts and "Hotspot" warnings.

---

## 🛠️ Prerequisites

- **Python 3.9+**
- **uv** (Package Manager) - Recommended for blazingly fast dependency installation.

## 📦 Installation & Setup

0. **Clone the repository**
   ```bash
   git clone https://github.com/Manoj-Bharathi-S/accident-detection-system.git
   ```

1. **Navigate to the Source Directory**
   Open your preferred terminal (`cmd` or PowerShell) and go to the project folder:
   ```bash
   cd accident-detection-system/
   ```

2. **Install Python Dependencies** using `uv`
   Create an environment and pull the required packages automatically:
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```
   *Note: Ensure your virtual environment is active if running directly via `python` (`.venv\Scripts\activate`), or simply prefix commands natively via `uv run`.*

3. **Configure Environment Variables**
   The project loads thresholds and secure SMTP credentials from a `.env` file.
   - Run the following command (or manually rename `.env.example` to `.env`):
     ```bash
     copy .env.example .env
     ```
   - Open `.env` and fill out your specific credentials! To test the alerting system.

4. **Prepare the Data**
   The program is hardcoded to natively look for an input video. 
   - Download a sample dashcam footage or traffic video (MP4 format).
   - Place it inside the `data\input\` directory.
   - Name it **`sample.mp4`**.
   *(If the file is not found, the script gracefully falls back to your local computer webcam).*

---

## 🚀 How to Run the Application

Once dependencies are mapped and your `sample.mp4` is in place, trigger the system:

```bash
python -m src.main
```

### While Running...
- A window titled **"Accident Detection System"** will appear.
- Bounding boxes (with generic IDs and local velocities) will be rendered over recognized vehicles.
- You can press the **`q`** key on your keyboard while focused on the video window to stop the program at any point.

### Analytics Generation
- Regardless of whether the video reaches the end naturally or you press `q`, an exit sequence starts.
- It will parse any collisions recorded within your `logs/accidents.csv` file.
- Look inside your `data/output/` directory for fresh graphical renderings (e.g., `causes_chart.png`) detailing the recent traffic statistics.
