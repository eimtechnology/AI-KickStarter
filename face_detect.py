import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
import cv2
import numpy as np
import os
import pickle

device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn = MTCNN(keep_all=True, device=device)
model = InceptionResnetV1(pretrained='vggface2').eval()

# Load registered faces
def load_registered_faces(file_path='registered_faces.pkl'):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return {}

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
        if boxes is not None:
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
                        else:
                            employee_name = "Unknown"
                            color = (0, 0, 255)  # Red box for unknown face

                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(frame, employee_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow('Recognize Employee', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    registered_faces = load_registered_faces()
    recognize_employee(registered_faces)
