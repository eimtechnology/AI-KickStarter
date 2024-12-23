import cv2
import mediapipe as mp
import math
import numpy as np
import time
import serial

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

port = "COM4"  # Adjust the port to match your setup
baudrate = 115200
# serial connection to talk to pico

ser = serial.Serial('COM4', 115200, timeout=1)

#serial_connection = serial.Serial(port, baudrate)

def calculate_angle(a, b, c):
    # Calculate the angle a-b-c, where b is the vertex
    ab = (a.x - b.x, a.y - b.y)
    bc = (c.x - b.x, c.y - b.y)

    dot_product = ab[0] * bc[0] + ab[1] * bc[1]
    magnitude_ab = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
    magnitude_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)
    
    cos_angle = dot_product / (magnitude_ab * magnitude_bc)
    angle = math.degrees(math.acos(max(-1.0, min(1.0, cos_angle))))  # 确保cos_angle在[-1, 1]范围内 / Ensure cos_angle is within [-1, 1]
    return angle

def finger_angel(landmarks, mcp_index, pip_index, dip_index):
    # Determine if a finger is bent (based on angle)
    angle = calculate_angle(landmarks[mcp_index], landmarks[pip_index], landmarks[dip_index])
    return angle

def count_fingers_states(hand_landmarks):
    landmarks = hand_landmarks.landmark
    finger_states = [
        finger_angel(landmarks, 1, 2, 3),  # 拇指 / Thumb
        finger_angel(landmarks, 0, 5, 6),  # 食指 / Index finger, palm|first joint
        finger_angel(landmarks, 0, 9, 10),  # 中指 / Middle finger
        finger_angel(landmarks, 0, 13, 14),  # 无名指 / Ring finger
        finger_angel(landmarks, 0, 17, 18) # 小指 / Pinky
    ]
    return finger_states

# Function to send a list of integers
def send_integers(int_list):
    for i in range (len(int_list)):
        int_list[i] = int(int_list[i])
    # Convert the list of integers into a comma-separated string
    
    data = str(int_list[1])
    
    if len(data) <= 2:
        data = "0"+data
        
    return data

def string_data(string):
    holder = str(string)
    if len(holder) < 3:
        holder = "0"+holder
        if len(holder) < 3:
            holder = "0"+holder
            if len(holder) < 3:
                holder = "0"+holder
            else:
                pass
        else:
            pass
    else:
        pass
    return holder

def string_angels(data):
    datalist = ""
    for i in range(len(data)):
        datalist = datalist + string_data(data[i])
    return datalist

def create_info_panel(finger_info, image_width, panel_height=50):
    panel = np.zeros((panel_height, image_width, 3), dtype=np.uint8)
    
    #Create a string to store the number of hands and the number of fingers for each hand
    info_text = f"Hands: {len(finger_info)} | "
    for i, count in enumerate(finger_info):
        info_text += f"Hand {i+1}: {count} fingers | "
    

    # If no hands are detected, display appropriate information
    if not finger_info:
        pass
    

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
        finger_count = []
        total_fingers = 0

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
                finger_count = count_fingers_states(hand_landmarks)
                for i in range (len(finger_count)):
                    finger_count[i] = int(finger_count[i])

        # 在终端打印信息
        # Print information in the terminal
        #print(f"Hands: {len(finger_info)} | Finger counts: {finger_info} | Total fingers: {total_fingers}")
    
        data = ""
        
        # send thumb finger angel
        if finger_count == []:
            pass
        else:
            data = string_angels(finger_count)
            
        print("Finger angles:", finger_count)
        '''
        print(type(finger_count))
        this = ""
        if len(finger_count) == 0:
            pass
        else:
            this = finger_count[2]
        print("The type of this is", type(this))
        '''
        print("This is the data string:", data)
        print(type(data))
        
        ser.write(data.encode('utf-8'))
        
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

cap.release()
ser.close()
cv2.destroyAllWindows()
