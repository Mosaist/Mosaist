import os
import json
import cv2
import torch

config = json.load(open(f'{os.path.dirname(__file__)}/../../config.json'))
"""
전역 환경 변수 모음
"""

class FaceRecognizer:
    """
    얼굴 인식 관련 클래스
    이미지 경로를 받아 얼굴 인식 수행.
    """

    default_model_path: str = f'{config["path"]["modelPath"]}/widerface-yolov5n/weights/best.pt'
    """
    widerface에 대한 기본 모델 경로.
    """

    target_faces = []

    def __init__(self, model_path: str=None, use_default: bool=True):
        """
        생성자

        Params:
            model_path: None이면 기본 모델 아니면 해당 경로의 모델 불러오기.
            use_default: True이면 기본 모델 로드.
        """

        self.model = None

        target_list = list(map(lambda t: f'{config["path"]["targetsetPath"]}/{t}', os.listdir(config['path']['targetsetPath'])))
        self.target_faces = [cv2.imread(target_path) for target_path in target_list]
        print(f'[FaceRecogniazer] Targetset loaded.')

        if use_default:
            self.model = torch.hub.load('ultralytics/yolov5', 'custom', FaceRecognizer.default_model_path)
            print(f'[FaceRecogniazer] Model init as default model.')
        else:
            print(f'[FaceRecogniazer] Model init as custom model.')

    def set_model(self, model_path: str):
        """
        모델 설정

        Params:
            model_path: 새로 설정할 모델의 경로. (문자열)
        """

        self.model = torch.hub.load('ultralytics/yolov5', 'custom', model_path)

    def set_model_m(self, model):
        """
        모델 설정

        Params:
            model_path_m: 새로 설정할 모델. (객체)
        """

        self.model = model

    def image_to_detections(self, images: list) -> list:
        """
        이미지를 바탕으로 얼굴 인식 수행

        Params:
            images: 얼굴 인식을 수행할 이미지 경로 또는 numpy.ndarray.

        Returns:
            이미지에 대한 인식 결과를 dict로 반환.
        """

        return [
            [
                {
                    'xmin': int(xmin),
                    'ymin': int(ymin),
                    'xmax': int(xmax),
                    'ymax': int(ymax),
                    'class': cls,
                    'name': name,
                } for xmin, ymin, xmax, ymax, cls, name in zip(result['xmin'], result['ymin'], result['xmax'], result['ymax'], result['class'], result['name'])
            ] for result in self.model(images).pandas().xyxy
        ]

    def image_to_labels(self, images: list) -> list:
        """
        이미지를 바탕으로 얼굴 인식 수행

        Params:
            images: 얼굴 인식을 수행할 이미지 경로 또는 numpy.ndarray.

        Returns:
            이미지에 대한 인식 결과를 list로 반환.
        """

        return [
            [
                [
                    cls,
                    (int(xmin) + int(xmax)) / 2 / width,
                    (int(ymin) + int(ymax)) / 2 / height,
                    (int(xmax) - int(xmin)) / width,
                    (int(ymax) - int(ymin)) / height
                ] for width, height, xmin, ymin, xmax, ymax, cls
                  in zip([image.shape[1]] * len(result['xmin']), [image.shape[0]] * len(result['xmin']), result['xmin'], result['ymin'], result['xmax'], result['ymax'], result['class'])
            ] for image, result in zip(images, self.model(images).pandas().xyxy)
        ]
