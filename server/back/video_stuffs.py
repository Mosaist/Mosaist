import os
import json
import cv2
import numpy as np

from facial_stuffs import FaceRecognizer

config = json.load(open(f'{os.path.dirname(__file__)}/../../config.json'))
"""
전역 환경 변수 모음
"""

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

    use_powershell = 'powershell' if os.name == 'nt' else ''
    os.system(f'{use_powershell} mv {path} {path}.temp')
    os.system(f'{use_powershell} ffmpeg -i {path}.temp -vcodec libx264 {path}')
    os.system(f'{use_powershell} rm {path}.temp')

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

def video_to_dataset(video_name: str, dataset_name: str, fr: FaceRecognizer, log: bool=False):
    """
    동영상을 데이터셋으로 변환
    inputs/videos의 특정 동영상을 데이터셋으로 변환.
    라벨은 얼굴의 경우, 기존에 학습된 모델을 활용.

    Params:
        video_name: 데이터셋으로 변환코자 하는 동영상 이름. (확장자 포함)
        dataset_name: 변환 후 데이터셋의 이름.
        fr: 얼굴 인식을 위한 사전 학습된 모델.
        log: 콘솔 로깅 여부.
    """

    video = cv2.VideoCapture(f'{config["path"]["inputPath"]}/videos/{video_name}')
    images = video_to_images(video)

    dataset_path = f'{config["path"]["datasetPath"]}/{dataset_name}'
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    image_path = f'{dataset_path}/images/'
    label_path = f'{dataset_path}/labels/'

    if not os.path.exists(image_path):
        os.makedirs(image_path)
    if not os.path.exists(label_path):
        os.mkdir(label_path)

    for i, image in enumerate(images):
        if log:
            print(f'[Video to Dataset]: {dataset_name} | {i} / {len(images) - 1}')

        img_path = f'{image_path}/{i}.png'
        lbl_path = f'{label_path}/{i}.txt'

        labels = [
            ' '.join(map(str, label))
            for label in fr.image_to_labels([image])[0]
        ]

        cv2.imwrite(img_path, image)
        with open(lbl_path, 'w') as f:
            f.write('\n'.join(labels))

    data_info_path = f'{config["path"]["yoloPath"]}/data/'
    data_info_file = open(data_info_path + '/' + dataset_path.split('/')[-1] + '.yaml', 'w')
    data_info_file.write(_get_yaml(dataset_path, image_path, image_path))

def video_to_targetset(video_name: str, fr: FaceRecognizer, log: bool=False):
    video = cv2.VideoCapture(f'{config["path"]["inputPath"]}/videos/{video_name}')
    images = video_to_images(video)

    targetset_path = config["path"]["targetsetPath"]
    o = list(map(lambda t: int(t.split('.')[0]), os.listdir(targetset_path)))
    o.sort()

    index = o[-1] if o else 0
    print(f'index origin: {index}')

    for i, image in enumerate(images):
        if log:
            print(f'[Video to targetset]: {i} / {len(images) - 1}')

        detection = fr.image_to_detections([image])[0]

        for det in detection:
            img_path = f'{targetset_path}/{index}.png'
            img = image[det['ymin']:det['ymax'], det['xmin']:det['xmax']]

            cv2.imwrite(img_path, img)

            index += 1

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
