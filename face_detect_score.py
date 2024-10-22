import cv2
import numpy as np
import insightface
from numpy.linalg import norm

# 初始化人脸检测和识别模型
detector = insightface.app.FaceAnalysis(allowed_modules=['detection', 'recognition'])
detector.prepare(ctx_id=0, det_size=(640, 640))

# 读取目标脸部图像
target_face_image = cv2.imread('long.jpg')
if target_face_image is None:
    print("Error: Could not read target face image.")
    exit()

# 检测目标脸部
target_faces = detector.get(target_face_image)
if len(target_faces) == 0:
    print("No face detected in target image.")
    exit()

# 获取目标脸部的嵌入向量
target_embedding = target_faces[0].normed_embedding

# 读取待处理图像
img = cv2.imread('musk3.jpg')
if img is None:
    print("Error: Could not read input image.")
    exit()

# 检测待处理图像中的脸部
faces = detector.get(img)

# 打印每个检测到的脸部的相似度分数，并在图像上绘制框
for face in faces:
    bbox = face.bbox.astype(np.int32)
    embedding = face.normed_embedding
    sim = np.dot(embedding, target_embedding) / (norm(embedding) * norm(target_embedding))
    score = (sim * 100).astype(np.int32)

    # 在图像上绘制绿色框
    cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

    # 在框的上方打印分数
    cv2.putText(img, f'Score: {score}', (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 显示结果图像
cv2.imshow('Face Detection with Score', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
