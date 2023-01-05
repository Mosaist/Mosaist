import os
import cv2
import numpy as np

from config import *

def video_to_images(video: cv2.VideoCapture) -> np.ndarray:
    """
    동영상을 이미지 리스트로 변환

    Params:
        video: 변환 대상 이미지리스트.

    Returns:
        이미지 리스트로 변환된 동영상.
    """

    images = []
    
    success, image = video.read()
    index = 0

    while success:
        images.append(image)
        success, image = video.read()
        index += 1

    return images

def save_images_as_video(images: list, path: str, fps: float=30) -> cv2.VideoWriter:
    """
    이미지 리스트를 동영상으로 저장

    Params:
        images: 이미지 리스트.
        path: 동영상을 저장할 경로.
        fps: 동영상의 FPS (기본, 30)
    """

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    size = (images[0].shape[1], images[0].shape[0])

    out = cv2.VideoWriter(path, fourcc, fps, size)
    for image in images:
        out.write(image)
    out.release()

def get_fps(video: cv2.VideoCapture) -> float:
    """
    동영상의 FPS 반환

    Params:
        FPS를 추출할 동영상.

    Returns:
        동영상의 FPS.
    """

    major_ver, _, _ = (cv2.__version__).split('.')
 
    if int(major_ver)  < 3 :
        return video.get(cv2.cv.CV_CAP_PROP_FPS)
    else :
        return video.get(cv2.CAP_PROP_FPS)

def video_to_dataset(video_name: str, dataset_name: str):
    """
    동영상을 데이터셋으로 변환
    inputs/videos의 특정 동영상을 데이터셋으로 변환.
    라벨은 동영상 크기 전체를 포괄하는 영역으로 설정.
    (0 0.5 0.5 1 1)

    Params:
        video_name: 데이터셋으로 변환코자 하는 동영상 이름. (확장자 포함)
        dataset_name: 변환 후 데이터셋의 이름.
    """

    video = cv2.VideoCapture(f'{INPUT_PATH}/videos/{video_name}')
    images = video_to_images(video)

    dataset_path = f'{DATASET_PATH}/{dataset_name}'
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    image_path = f'{dataset_path}/images/'
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    for i, image in enumerate(images):
        cv2.imwrite(image_path + str(i) + '.png', image)

    _init_dataset(dataset_path)

def _init_dataset(dataset_path: str):
    """
    *내부 함수

    이미지 묶음으로 변환된 동영상 프레임에 라벨 부여.

    Params:
        dataset_path: 대상 데이터셋 경로.
    """

    image_path = dataset_path + 'images/'

    if not os.path.exists(dataset_path):
        raise ValueError(f'Path not exist: {dataset_path}')
    if not os.path.exists(image_path):
        raise ValueError(f'Path not exist: {image_path}')

    label_path = dataset_path + 'labels/'

    if not os.path.exists(label_path):
        os.mkdir(label_path)

    image_names = os.listdir(image_path)

    for image_name in image_names:
        label_file = open(label_path + image_name.split('.')[0] + '.txt', 'w')
        label_file.write('0 0.5 0.5 1 1')
        label_file.close()

    data_info_path = f'{YOLO_PATH}/data'
    data_info_file = open(data_info_path + dataset_path.split('/')[-1] + '.yaml', 'w')
    data_info_file.write(_get_yaml(dataset_path, image_path, image_path))

def _get_yaml(dataset_path: str, image_path: str, val_path: str) -> str:
    """
    *내부 함수

    데이터셋에 대한 yaml 설정 문자열 생성

    Params:
        dataset_path: 대상 데이터셋 경로.
        image_path: 이미지 파일 디렉토리 경로.
        val_path: 검증 파일 디렉토리 경로.

    Returns:
        yaml 설정 문자열.
    """

    return f'''path: {dataset_path}
train: {image_path}
val: {val_path}

names:
    0: object
'''
