import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
import cv2
import numpy as np
import os
import pickle

device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn = MTCNN(keep_all=True, device=device)
model = InceptionResnetV1(pretrained='vggface2').eval()

# Loading registered faces
def load_registered_faces(file_path='registered_faces.pkl'):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return {}

# Saving registered faces
def save_registered_faces(face_data, file_path='registered_faces.pkl'):
    with open(file_path, 'wb') as f:
        pickle.dump(face_data, f)

# Register employee by capturing face
def register_employee(employee_name):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return
    
    face_embeddings = []
    print("Capturing employee's face... Press 'q' to capture, 'Esc' to finish.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break
        cv2.imshow('Register Employee', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            boxes, _ = mtcnn.detect(frame)
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box)
                    face = frame[y1:y2, x1:x2]
                    face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                    face_resized = cv2.resize(face_rgb, (156, 156))
                    face_tensor = torch.tensor(face_resized).permute(2, 0, 1).float().unsqueeze(0) / 255.0

                    with torch.no_grad():
                        embedding = model(face_tensor).squeeze().numpy()
                    face_embeddings.append(embedding)
                    print(f"Captured face. Current captures: {len(face_embeddings)}")
            else:
                print("No face detected. Try again.")

        if cv2.waitKey(1) & 0xFF == 27:
            break

    if face_embeddings:
        face_embedding_avg = np.mean(face_embeddings, axis=0)
        registered_faces = load_registered_faces()
        registered_faces[employee_name] = face_embedding_avg
        save_registered_faces(registered_faces)
        print(f"Employee {employee_name} registered successfully with {len(face_embeddings)} captures.")
    else:
        print("No valid face captures.")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    employee_name = input("Enter employee name: ")
    register_employee(employee_name)
