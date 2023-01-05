# %%
# Import libs.
import sys
import cv2

sys.path.append('../image_handling')
from facial_stuffs import *
from image_stuffs import *
from config import *

# %%
# Set vars.
dataset_name = 'test2'
path_root = f'{DATASET_PATH}/{dataset_name}'
path_images = f'{DATASET_PATH}/{dataset_name}/images'
path_labels = f'{DATASET_PATH}/{dataset_name}/labels'
path_rect = f'{DATASET_PATH}/{dataset_name}/rect'

f = FaceRecognizer()

# %%
# Load images.
images = [
    { 'name': image_name, 'image': cv2.imread(f'{path_images}/{image_name}') }
    for image_name in os.listdir(path_images)
]

for image in images:
    image['detections'] = f.image_to_detections([image['image']])

# %%
# Save labels and rected images.
if not os.path.exists(path_labels):
    os.mkdir(path_labels)
if not os.path.exists(path_rect):
    os.mkdir(path_rect)

for image in images:
    image_width = image['image'].shape[1]
    image_height = image['image'].shape[0]

    labels = []
    for detection in image['detections'][0]:
        x = (detection['xmin'] + detection['xmax']) / 2 / image_width
        y = (detection['ymin'] + detection['ymax']) / 2 / image_height
        w = (detection['xmax'] - detection['xmin']) / image_width
        h = (detection['ymax'] - detection['ymin']) / image_height

        labels.append(f'{detection["class"]} {x} {y} {w} {h}')

    with open(f'{path_labels}/{image["name"][:-4]}.txt', 'w') as f:
        f.write('\n'.join(labels))

    image_rected = rect_image(image['image'], image['detections'][0])
    cv2.imwrite(f'{path_rect}/{image["name"]}', image_rected)

# %%
