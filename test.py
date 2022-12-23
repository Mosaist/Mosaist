# %%
# Load libs.
import os
import cv2

from facial_stuffs import *
from image_stuffs import *

# %%
# Set variables.
path = '../inputs'
img_names = os.listdir(path)

num_imgs = 4
imgs = [f'{path}/{img_name}' for img_name in img_names[:num_imgs]]
imgs_pd = [cv2.imread(path) for path in imgs]

f = FaceRecognizer()

# %%
# Face recognition.
detections = f.image_to_detections(imgs)

for idx, (img, detection) in enumerate(zip(imgs_pd, detections)):
    res = blur_image(img, detection)
    cv2.imwrite(f'../outputs/widerface_{idx}_blur.jpg', res)

# %%
# Face recognition. (Coco128)
# 실시간 모델 변경 (실험적)
# 
# 두 가지 모델 변경 방법 제공:
#   모델 경로: 해당 모델을 즉석에서 로드하여 모델 변경.
#   모델 객체: 미리 로드된 모델로 변경.
# 
# 전자의 경우 여러 번 모델 변경 시 VRAM 초과 발생 주의. 모델 언로드 방법 찾아볼 것.
# 아래의 함수는 후자.
f.set_model_m(FaceRecognizer.default_models['coco128'])

detections = f.image_to_detections(imgs)

for idx, (img, detection) in enumerate(zip(imgs_pd, detections)):
    res = blur_image(img, detection)
    cv2.imwrite(f'../outputs/coco128_{idx}_blur.jpg', res)
