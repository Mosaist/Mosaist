# %%
import sys
import time
import cv2

sys.path.append('../image_handling')
from facial_stuffs import *
from image_stuffs import *

# 전면만 있으면 0, 전후면 모두 있으면 1.
webcam = cv2.VideoCapture(0)

f = FaceRecognizer()

custom_model_name = 'coco128-yolov5s'
# f.set_model(MODEL_PREFIX + f'{custom_model_name}/weights/best.pt')

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

prev_time = 0
fps = 24

while webcam.isOpened():
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    status, frame = webcam.read()

    curr_time = time.time() - prev_time
    if not (status and (curr_time > 1 / fps)):
        continue
    prev_time = time.time()

    detections = f.image_to_detections(frame)
    frame = rect_image(frame, detections[0])

    cv2.imshow("test", frame)

webcam.release()
cv2.destroyAllWindows()

# %%
