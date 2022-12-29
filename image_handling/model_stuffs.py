import os

from config import *

def train_images(dataset_name: str):
    """
    특정 데이터셋을 이용해 학습 수행

    Params:
        dataset_name: 학습을 수행할 데이터셋 이름.
    """

    os.system(f'python {YOLO_PREFIX}train.py --data {dataset_name}.yaml --epochs 500 --weights yolov5n.pt --batch-size 128 --name {dataset_name}')
