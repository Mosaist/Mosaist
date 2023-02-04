import cv2
import numpy as np

def rect_image(image: np.ndarray, detections: list) -> np.ndarray:
    """
    이미지와 인식 결과를 합성
    인식된 이미지에 사각 프레임 합성.

    Param:
        image: 인식 대상 이미지.
        detections: 인식 결과 리스트.

    Returns:
        합성된 이미지.
    """

    img = image.copy()
    for detection in detections:
        img = cv2.rectangle(
            img,
            (detection['xmin'], detection['ymin']),
            (detection['xmax'], detection['ymax']),
            (0, 255, 0), 3
        )

    return img

def mosaic_image(image: np.ndarray, detections: list) -> np.ndarray:
    """
    이미지와 인식 결과를 합성
    인식된 이미지를 모자이크 처리.

    Param:
        image: 인식 대상 이미지.
        detections: 인식 결과 리스트.

    Returns:
        합성된 이미지.
    """

    return_image = image.copy()

    for detection in detections:
        if not detection:
            continue

        x1, y1 = detection['xmin'], detection['ymin']
        x2, y2 = detection['xmax'], detection['ymax']

        return_image[y1:y2, x1:x2] = _pixelate(return_image[y1:y2, x1:x2])

    return return_image

def _pixelate(image: np.ndarray) -> np.ndarray:
    """
    *내부 함수

    이미지 모자이크 처리

    Param:
        image: 대상 이미지.

    Returns:
        합성된 이미지.
    """

    height, width, _ = image.shape

    temp = cv2.resize(image, (8, 8), interpolation=cv2.INTER_LINEAR)

    return cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
