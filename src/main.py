import cv2
import numpy as np
import random
from ultralytics import YOLO
from src.config import VIDEO_SOURCE, YOLO_MODEL, CONFIDENCE_THRESHOLD, COLLISION_FRAME_OVERLAP
from src.analyzer import calculate_speed, check_collision, estimate_severity, infer_cause
from src.alerter import send_alert_email
from src.logger import log_accident, generate_analytics

def main():
    print(f"Loading YOLO model: {YOLO_MODEL}")
    model = YOLO(YOLO_MODEL)
    
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        print(f"Error: Could not open video source {VIDEO_SOURCE}")
        print("Falling back to webcam (source 0)...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("No video source available. Exiting.")
            return
            
    # Track states
    history = {} # id -> [last_box, speed]
    collision_matrix = {} # (id1, id2) -> overlap_frames
    logged_collisions = set()
    
    print("Starting video feed... Press 'q' to quit.")
    frame_count = 0
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print(f"[DEBUG] cap.read() returned False at frame {frame_count}. End of video or read error.")
                break
            frame_count += 1
            
            # Run YOLO with tracking, persist=True ensures IDs match across frames
            # Classes: 2=car, 3=motorcycle, 5=bus, 7=truck
            results = model.track(frame, persist=True, conf=CONFIDENCE_THRESHOLD, classes=[2, 3, 5, 7], verbose=False) 
            
            if results[0].boxes.id is not None:
                boxes = results[0].boxes.xyxy.cpu().numpy()
                ids = results[0].boxes.id.cpu().numpy().astype(int)
                
                # Map current boxes and update history/speed
                current_objects = {}
                for box, obj_id in zip(boxes, ids):
                    current_objects[obj_id] = box
                    speed = 0
                    max_speed = 0
                    if obj_id in history:
                        speed = calculate_speed(history[obj_id][0], box)
                        # Retain the highest speed recorded for this object
                        prev_max = history[obj_id][2] if len(history[obj_id]) > 2 else speed
                        max_speed = max(prev_max, speed)
                    history[obj_id] = (box, speed, max_speed)
                    
                    # Draw Box
                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"ID:{obj_id} Spd:{speed:.1f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Check collisions between all pairs
                curr_ids = list(current_objects.keys())
                for i in range(len(curr_ids)):
                    for j in range(i+1, len(curr_ids)):
                        id1, id2 = curr_ids[i], curr_ids[j]
                        box1, box2 = current_objects[id1], current_objects[id2]
                        
                        pair = tuple(sorted((id1, id2)))
                        
                        if check_collision(box1, box2):
                            collision_matrix[pair] = collision_matrix.get(pair, 0) + 1
                            
                            # Draw overlapping warning
                            if collision_matrix[pair] > 1:
                                center_x = int((box1[0]+box2[0])/2)
                                center_y = int((box1[1]+box2[1])/2)
                                cv2.circle(frame, (center_x, center_y), 30, (0, 165, 255), 3) # Orange warning circle
                            
                            if collision_matrix[pair] >= COLLISION_FRAME_OVERLAP and pair not in logged_collisions:
                                # A confirmed collision occurred!
                                logged_collisions.add(pair)
                                # Use max_speed recorded before impact for severity logic
                                speed1 = history[id1][2] if len(history[id1]) > 2 else history[id1][1]
                                speed2 = history[id2][2] if len(history[id2]) > 2 else history[id2][1]
                                
                                severity = estimate_severity(speed1, speed2)
                                cause = infer_cause(speed1, speed2)
                                
                                # Simulated Mock Coordinates (Around Chennai for this prototype)
                                coords = (13.0827 + random.uniform(-0.01, 0.01), 80.2707 + random.uniform(-0.01, 0.01))
                                
                                print(f"\n[! CRITICAL !] COLLISION DETECTED between ID {id1} and {id2}")
                                print(f"Severity: {severity}, Cause: {cause}")
                                
                                # Log the accident
                                log_accident(severity, cause, coords)
                                
                                # Alert for ALL severities for now
                                send_alert_email(severity, cause, coords)
                                    
                        else:
                            collision_matrix[pair] = 0 # reset if they stop overlapping
            
            # Display global Alert on frame if an accident happened recently
            if len(logged_collisions) > 0:
                cv2.putText(frame, "ACCIDENT LOGGED", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                
            cv2.imshow("Accident Detection System", frame)
            
            # Stop on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user (Ctrl+C).")
    finally:
        if cap:
            cap.release()
        cv2.destroyAllWindows()
        
        # Generate Analytics after processing
        print("\nProcessing complete. Generating analytics report...")
        generate_analytics()

if __name__ == "__main__":
    main()
