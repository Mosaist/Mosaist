import os
import json

config = json.load(open(f'{os.path.dirname(__file__)}/../../config.json'))
"""
전역 환경 변수 모음
"""

def train_images(dataset_name: str):
    """
    특정 데이터셋을 이용해 학습 수행

    Params:
        dataset_name: 학습을 수행할 데이터셋 이름.
    """

    # default
    # epoch: 10, batch : 128

    num_epochs = 5
    num_batch = 4

    os.system(f'python {config["path"]["yoloPath"]}/train.py --data {dataset_name}.yaml --epochs {num_epochs} --weights yolov5n.pt --batch-size {num_batch} --name {dataset_name}')
