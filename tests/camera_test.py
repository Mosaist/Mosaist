# %%
import sys
import time
import cv2

sys.path.append('../image_handling')
from facial_stuffs import *
from image_stuffs import *

webcam = cv2.VideoCapture(1)
f = FaceRecognizer()

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
    frame = mosaic_image(frame, detections[0])

    cv2.imshow("test", frame)

webcam.release()
cv2.destroyAllWindows()

# %%
