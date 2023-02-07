# %%
# Import libs.
import os
import sys
import cv2
import json

sys.path.append('../server/back')
from facial_stuffs import *
from image_stuffs import *

config = json.load(open('../config.json'))

# %%
# Set vars.
dataset_name = 'test2_labeling'
path_root = f'{config["path"]["datasetPath"]}/{dataset_name}'
path_images = f'{config["path"]["datasetPath"]}/{dataset_name}/images'
path_labels = f'{config["path"]["datasetPath"]}/{dataset_name}/labels'
path_rect = f'{config["path"]["datasetPath"]}/{dataset_name}/rect'

f = FaceRecognizer()

# %%
# Load images.
images = [
    { 'name': image_name, 'image': cv2.imread(f'{path_images}/{image_name}') }
    for image_name in os.listdir(path_images)
]

for image in images:
    image['labels'] = f.image_to_labels([image['image']])

# %%
# Save labels and rected images.
if not os.path.exists(path_labels):
    os.mkdir(path_labels)
if not os.path.exists(path_rect):
    os.mkdir(path_rect)

for image in images:
    labels = [
        ' '.join(map(str, label))
        for label in image['labels'][0]
    ]

    with open(f'{path_labels}/{image["name"][:-4]}.txt', 'w') as f:
        f.write('\n'.join(labels))

    # image_rected = rect_image(image['image'], image['detections'][0])
    # cv2.imwrite(f'{path_rect}/{image["name"]}', image_rected)

# %%
