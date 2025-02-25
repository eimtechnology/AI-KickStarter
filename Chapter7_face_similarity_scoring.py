import cv2
import numpy as np
import insightface
from numpy.linalg import norm

# Initialize face detection and recognition model
detector = insightface.app.FaceAnalysis(allowed_modules=['detection', 'recognition'])
detector.prepare(ctx_id=0, det_size=(640, 640))

# Read the target face image
target_face_image = cv2.imread('long.jpg')
if target_face_image is None:
    print("Error: Could not read target face image.")
    exit()

# Detect target face
target_faces = detector.get(target_face_image)
if len(target_faces) == 0:
    print("No face detected in target image.")
    exit()

# Obtain the embedding vector of the target face
target_embedding = target_faces[0].normed_embedding

# Read the image to be processed
# replace the file name by your image
img = cv2.imread('person1.jpg')
if img is None:
    print("Error: Could not read input image.")
    exit()

# Detect faces in the image to be processed
faces = detector.get(img)

# Print the similarity score for each detected face and draw a box on the faces
for face in faces:
    bbox = face.bbox.astype(np.int32)
    embedding = face.normed_embedding
    sim = np.dot(embedding, target_embedding) / (norm(embedding) * norm(target_embedding))
    score = (sim * 100).astype(np.int32)

    # Draw a green box on the faces
    cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

    # Print scores above the boxes
    cv2.putText(img, f'Score: {score}', (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Show the result
cv2.imshow('Face Detection with Score', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
