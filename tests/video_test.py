# %%
# Imoprt libs.
import sys

sys.path.append('../image_handling')
from facial_stuffs import *
from image_stuffs import *
from video_stuffs import *

# %%
# Load video and convert into image list.
video = cv2.VideoCapture('../inputs/videos/test.mp4')
images = video_to_images(video)

# %%
# Face recognition.
f = FaceRecognizer()
detections = f.image_to_detections(images)

# %%
# Blur and save as video.
mosaiced_images = [mosaic_image(img, det) for img, det in zip(images, detections)]
save_images_as_video(mosaiced_images, '../outputs/videos/test.mp4')

# %%
