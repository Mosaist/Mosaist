import cv2
import numpy as np

def draw_rect_with_detection(image: np.ndarray, detections: list) -> np.ndarray:
    """
    이미지와 인식 결과를 합성

    Param:
        imgae:
        detections:

    Returns:
        합성된 이미지

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
