import os

from math import ceil

from config import *

def train_images(dataset_name: str):
    """
    특정 데이터셋을 이용해 학습 수행

    Params:
        dataset_name: 학습을 수행할 데이터셋 이름.
    """

    # epoch, batch 수정
    # epoch: 500, batch: 128
    # epoch: 5, batch: 1000
    # epoch: 10, batch : 64

    path = f'{DATASET_PATH}/{dataset_name}'
    img_names = os.listdir(path)

    num_epochs = 10 #5 #4
    num_batch = 64 #32

    os.system(f'python {YOLO_PATH}/train.py --data {dataset_name}.yaml --epochs {num_epochs} --weights yolov5n.pt --batch-size {num_batch} --name {dataset_name}')
