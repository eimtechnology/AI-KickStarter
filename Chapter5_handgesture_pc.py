import cv2
import mediapipe as mp
import math
import numpy as np
import time
import serial
from serial.tools import list_ports

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# port = "/dev/cu.usbmodem1101"  # Adjust the port to match your setup
port = list_ports.comports()[0].device

baudrate = 115200
#serial connection to talk to pico
serial_connection = serial.Serial(port, baudrate)
def calculate_distance(point1, point2):
    "Calculate the Euclidean distance between two points"
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def calculate_angle(a, b, c):
    """Calculate the angle a-b-c, where b is the vertex"""
    ab = (a.x - b.x, a.y - b.y)
    bc = (c.x - b.x, c.y - b.y)

    dot_product = ab[0] * bc[0] + ab[1] * bc[1]
    magnitude_ab = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
    magnitude_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)
    
    cos_angle = dot_product / (magnitude_ab * magnitude_bc)
    angle = math.degrees(math.acos(max(-1.0, min(1.0, cos_angle))))  # Ensure cos_angle is within [-1, 1]
    return angle

def is_finger_straight(landmarks, finger_tip_index, finger_mcp_index, wrist_index=0):
    """Determine if a finger is straight (based on distance)"""
    wrist = landmarks[wrist_index]
    finger_tip = landmarks[finger_tip_index]
    finger_mcp = landmarks[finger_mcp_index]

    tip_to_wrist_distance = calculate_distance(finger_tip, wrist)
    mcp_to_wrist_distance = calculate_distance(finger_mcp, wrist)

    return tip_to_wrist_distance > mcp_to_wrist_distance

def is_finger_bent(landmarks, mcp_index, pip_index, dip_index):
    """Determine if a finger is bent (based on angle)"""
    angle = calculate_angle(landmarks[mcp_index], landmarks[pip_index], landmarks[dip_index])
    return angle < 160  # 小于160度认为手指弯曲 / Consider the finger bent if angle is less than 160 degrees

def count_fingers(hand_landmarks):
    landmarks = hand_landmarks.landmark
    finger_states = [
        not is_finger_bent(landmarks, 1, 2, 3) and is_finger_straight(landmarks, 4, 1),  # Thumb
        not is_finger_bent(landmarks, 5, 6, 7) and is_finger_straight(landmarks, 8, 5),  # Index finger
        not is_finger_bent(landmarks, 9, 10, 11) and is_finger_straight(landmarks, 12, 9),  # Middle finger
        not is_finger_bent(landmarks, 13, 14, 15) and is_finger_straight(landmarks, 16, 13),  # Ring finger
        not is_finger_bent(landmarks, 17, 18, 19) and is_finger_straight(landmarks, 20, 17)  # Pinky
    ]
    finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    straight_fingers = [finger_names[i] for i, state in enumerate(finger_states) if state]
    return sum(finger_states), straight_fingers

def create_info_panel(finger_info, image_width, panel_height=50):
    panel = np.zeros((panel_height, image_width, 3), dtype=np.uint8)

    # Create a string to store the number of hands and the number of fingers for each hand
    info_text = f"Hands: {len(finger_info)} | "
    for i, count in enumerate(finger_info):
        info_text += f"Hand {i+1}: {count} fingers | "
    
    # If no hands are detected, display appropriate information
    if not finger_info:
        info_text = "No hands detected"
    
    # Draw text on the panel
    cv2.putText(panel, info_text.strip(), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    return panel

# Camera input section
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
    
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
    
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        finger_info = []
        total_fingers = 0
    
        finger_list = []
    
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
                finger_count, straight_fingers = count_fingers(hand_landmarks)  
    
                finger_list.append(straight_fingers)
                finger_info.append(finger_count)
                total_fingers += finger_count
    

        # Print information in the terminal
        print(f"Hands: {len(finger_info)} | Finger counts: {finger_info} | Total fingers: {total_fingers} | Finger list: {finger_list}")
    
        if not len(finger_list) == 0:
            serial_connection.write(('1' if "Thumb" in finger_list[0] else '0').encode())
            serial_connection.write(('1' if "Index" in finger_list[0] else '0').encode())
            serial_connection.write(('1' if "Middle" in finger_list[0] else '0').encode())
            serial_connection.write(('1' if "Ring" in finger_list[0] else '0').encode())
            serial_connection.write(('1' if "Pinky" in finger_list[0] else '0').encode())
            serial_connection.write(("\n").encode())
           
        # Get image width
        image_width = image.shape[1]
    
        # Create information panel
        info_panel = create_info_panel(finger_info, image_width)
    
        # Flip the main image
        image = cv2.flip(image, 1)
    
        # Vertically stack the main image and information panel
        display_image = np.vstack((image, info_panel))
    
        cv2.imshow('MediaPipe Hands', display_image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

# close the windows and stop the program
cap.release()
serial_connection.close()
cv2.destroyAllWindows()
