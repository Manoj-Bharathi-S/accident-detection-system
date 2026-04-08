import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from src.config import LOG_FILE

def log_accident(severity, cause, coordinates):
    file_exists = os.path.isfile(LOG_FILE)
    
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Latitude", "Longitude", "Severity", "Cause"])
        
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            coordinates[0],
            coordinates[1],
            severity,
            cause
        ])
    print(f"[LOG] Accident logged to {LOG_FILE}.")

def generate_analytics():
    if not os.path.isfile(LOG_FILE):
        print("[ANALYTICS] No data to analyze.")
        return
        
    try:
        df = pd.read_csv(LOG_FILE)
        if df.empty:
            return
            
        # Generate Cause Pie Chart
        cause_counts = df['Cause'].value_counts()
        if not cause_counts.empty:
            plt.figure(figsize=(8, 6))
            cause_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140)
            plt.title('Accident Causes Breakdown')
            plt.ylabel('')
            plt.tight_layout()
            chart_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'output', 'causes_chart.png')
            plt.savefig(chart_path)
            plt.close()
            print(f"[ANALYTICS] Chart saved to {chart_path}")
        
        # Identify hotspots
        df['Lat_round'] = df['Latitude'].round(3)
        df['Lon_round'] = df['Longitude'].round(3)
        hotspots = df.groupby(['Lat_round', 'Lon_round']).size().sort_values(ascending=False).head(5)
        
        print("\n--- AI SAFETY SUGGESTIONS ---")
        if not hotspots.empty:
            top_spot = hotspots.index[0]
            count = hotspots.iloc[0]
            print(f"> HOTSPOT DETECTED: Location ({top_spot[0]}, {top_spot[1]}) had {count} accidents logged.")
            if count >= 3:
                print(f"> SUGGESTION: High frequency at ({top_spot[0]}, {top_spot[1]}). Consider installing speed cameras or physical speed bumps.")
        print("-----------------------------\n")
    except Exception as e:
        print(f"[ANALYTICS ERROR] Could not generate analytics: {e}")
