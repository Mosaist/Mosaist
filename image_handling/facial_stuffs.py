import torch

from config import *

class FaceRecognizer:
    """
    얼굴 인식 관련 클래스
    이미지 경로를 받아 얼굴 인식 수행.
    """

    default_model_paths: dict = {
        'widerface': MODEL_PREFIX + 'widerface-yolov5n/weights/best.pt',
        'coco128': MODEL_PREFIX + 'coco128-yolov5n/weights/best.pt',
    }
    """
    widerface와 coco128에 대한 기본 모델 경로.
    """

    default_models: dict = {
        'widerface': torch.hub.load('ultralytics/yolov5', 'custom', default_model_paths['widerface']),
        'coco128': torch.hub.load('ultralytics/yolov5', 'custom', default_model_paths['coco128']),
    }
    """
    기본 모델 미리 불러오기.
    """

    default_model = default_models['widerface']
    """
    기본 모델로 widerface 채택.
    """

    def __init__(self, model_path: str=None):
        """
        생성자

        Params:
            model_path: None이면 기본 모델 아니면 해당 경로의 모델 불러오기.
        """

        self.model = self.default_model if model_path is None else torch.hub.load('ultralytics/yolov5', 'custom', model_path)

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
