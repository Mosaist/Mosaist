import os
import json

ROOT = os.path.abspath(os.path.abspath(os.path.dirname(__file__)) + '/..')
"""
프로젝트 루트 경로
"""

_json = json.load(open(f'{ROOT}/config.json'))
"""
*내부 변수

config.json
"""

# 경로 관련 변수

YOLO_PATH = f'{ROOT}/{_json["path"]["yoloPath"]}'
"""
YOLOv5에 대한 경로
"""

MODEL_PATH = f'{ROOT}/{_json["path"]["modelPath"]}'
"""
미리 학습된 모델에 대한 경로
"""

DATASET_PATH = f'{ROOT}/{_json["path"]["datasetPath"]}'
"""
데이터셋에 대한 경로
"""

INPUT_PATH = f'{ROOT}/{_json["path"]["inputPath"]}'
"""
입력 디렉토리에 대한 경로
"""

OUTPUT_PATH = f'{ROOT}/{_json["path"]["outputPath"]}'
"""
출력 디렉토리에 대한 경로
"""

# API 서버 관련 변수

ALLOWED_IMAGE_EXTENSIONS = set(_json["back"]["allowedImageExtensions"])
"""
허용된 이미지 형식
"""

ALLOWED_VIDEO_EXTENSIONS = set(_json["back"]["allowedVideoExtensions"])
"""
허용된 동영상 형식
"""

EDIT_PREFIX = _json['back']['editPrefix']
"""
출력 디렉토리에 저장될 파일의 접두어
"""

IP = _json['back']['ip']
"""
API 서버 IP
"""

PORT = _json['back']['port']
"""
API 서버 포트
"""

def print_config():
    print()
    print(f'Path Configurations:')
    print(f'    Root Path:    {ROOT}')
    print(f'    Yolo Path:    {YOLO_PATH}')
    print(f'    Model Path:   {MODEL_PATH}')
    print(f'    Dataset Path: {DATASET_PATH}')
    print(f'    Input Path:   {INPUT_PATH}')
    print(f'    Output Path:  {OUTPUT_PATH}')
    print()

    print(f'API Configurations:')
    print(f'    Allowed Image Extensions: {ALLOWED_IMAGE_EXTENSIONS}')
    print(f'    Allowed Video Extensions: {ALLOWED_VIDEO_EXTENSIONS}')
    print(f'    Edit Prefix:              {EDIT_PREFIX}') 
    print(f'    API Server IP:            {IP}')
    print(f'    API Server Port:          {PORT}')
    print()
