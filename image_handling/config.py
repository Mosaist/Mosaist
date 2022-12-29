import os

PREFIX = os.path.abspath(os.path.dirname(__file__)) + '/'
"""
image_handling에 대한 절대 경로
"""

YOLO_PREFIX = PREFIX + '../yolov5/'
"""
YOLOv5에 대한 절대 경로
"""

MODEL_PREFIX = YOLO_PREFIX + 'runs/train/'
"""
미리 학습된 모델에 대한 절대 경로
"""

DATASET_PREFIX = PREFIX + '../datasets/'
"""
데이터셋에 대한 절대 경로
"""

INPUT_DIR = PREFIX + '../inputs/'
"""
입력 디렉토리에 대한 절대 경로
"""

OUTPUT_DIR = PREFIX + '../outputs/'
"""
출력 디렉토리에 대한 절대 경로
"""

PORT = 80
"""
API 서버 포트
"""
