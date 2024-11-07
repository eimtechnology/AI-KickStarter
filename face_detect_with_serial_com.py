import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
import cv2
import numpy as np
import os
import pickle
import serial


port = "COM5"  # Adjust the port to match your setup
baudrate = 115200
ser = serial.Serial('COM5', 115200, timeout=1)

# pre-setting
serial_data = ""
serial_data_list = [0,0] # green_light, red_light
name_list = ["","",""]

device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn = MTCNN(keep_all=True, device=device)
model = InceptionResnetV1(pretrained='vggface2').eval()

# Load registered faces
def load_registered_faces(file_path='registered_faces.pkl'):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return {}

def append_space2(names):
    return [name.ljust(12) for name in names]

# Recognize employee using face embedding
def recognize_employee(registered_faces):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return

    print("Recognizing employee... Press 'Esc' to exit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        boxes, _ = mtcnn.detect(frame)
        
        serial_data_list[0] = 0
        serial_data_list[1] = 0
        name_list = ["","",""]
        
        if boxes is not None:
            i = 0
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                if x1 >= 0 and y1 >= 0 and x2 <= frame.shape[1] and y2 <= frame.shape[0]:
                    face = frame[y1:y2, x1:x2]
                    if face.size > 0:
                        face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                        face_resized = cv2.resize(face_rgb, (156, 156))
                        face_tensor = torch.tensor(face_resized).permute(2, 0, 1).float().unsqueeze(0) / 255.0

                        with torch.no_grad():
                            embedding = model(face_tensor).squeeze().numpy()

                        threshold = 0.7
                        min_distance = float('inf')
                        recognized_employee = None
                        
                        for employee_name, registered_embedding in registered_faces.items():
                            distance = np.linalg.norm(embedding - registered_embedding)
                            if distance < min_distance:
                                min_distance = distance
                                recognized_employee = employee_name
                        
                        if recognized_employee and min_distance < threshold:
                            employee_name = recognized_employee
                            color = (0, 255, 0)  # Green box for recognized employee
                            serial_data_list[0] = 1
                            name_list[i] = recognized_employee
                            i = i+1
                            
                        else:
                            employee_name = "Unknown"
                            color = (0, 0, 255)  # Green box for recognized employee
                            serial_data_list[1] = 1

                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(frame, employee_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        
        cv2.imshow('Recognize Employee', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break
        
        serial_data = ''.join(map(str, serial_data_list))
        #print(name_list)
        padded_names = append_space2(name_list)
        #print("Element length:", len(padded_names[0]))
        for i in range(len(padded_names)):
            serial_data += padded_names[i]
        print(serial_data)
        #print("serial_data length:", len(serial_data))
        ser.write(serial_data.encode('utf-8'))
        

    cap.release()
    ser.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    registered_faces = load_registered_faces()
    recognize_employee(registered_faces)
