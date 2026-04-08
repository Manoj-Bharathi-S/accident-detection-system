import numpy as np

def calculate_speed(prev_box, curr_box):
    # Box format: [x1, y1, x2, y2]
    # Calculate centroid distance between previous and current bounding box
    prev_cx = (prev_box[0] + prev_box[2]) / 2
    prev_cy = (prev_box[1] + prev_box[3]) / 2
    
    curr_cx = (curr_box[0] + curr_box[2]) / 2
    curr_cy = (curr_box[1] + curr_box[3]) / 2
    
    # Distance in pixels (proxy for speed)
    distance = np.sqrt((curr_cx - prev_cx)**2 + (curr_cy - prev_cy)**2)
    return distance

def check_collision(box1, box2):
    # Check if two bounding boxes overlap
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2
    
    if x1_max < x2_min or x2_max < x1_min:
        return False
    if y1_max < y2_min or y2_max < y1_min:
        return False
        
    return True

def estimate_severity(speed1, speed2):
    # Simple rule based logic for prototype
    avg_speed = (speed1 + speed2) / 2
    
    if avg_speed > 10:
        return "HIGH"
    elif avg_speed > 4:
        return "MEDIUM"
    else:
        return "LOW"
        
def infer_cause(speed1, speed2):
    avg_speed = (speed1 + speed2) / 2
    if avg_speed > 10:
        return "Over-speeding"
    elif abs(speed1 - speed2) > 5: # High relative delta
        return "Sudden Braking / Speed Mismatch"
    else:
        return "Poor Visibility / Distraction"
