import os

from config import *

def train_images(dataset_name: str):
    os.system(f'python {YOLO_PREFIX}train.py --data {dataset_name}.yaml --epochs 3 --weights yolov5n.pt --batch-size 1 --name {dataset_name}')
