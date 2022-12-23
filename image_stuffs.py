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

def blur_image(image: np.ndarray, detections: list) -> np.ndarray:
    """
    이미지와 인식 결과를 합성
    인식된 이미지를 블러 처리.

    Param:
        image: 인식 대상 이미지.
        detections: 인식 결과 리스트.

    Returns:
        합성된 이미지
    """

    image_mask = np.zeros(image.shape[:2], np.uint8)
    image_mask.fill(255)
    blur_mask = np.zeros(image.shape[:2], np.uint8)

    for detection in detections:
        image_mask[detection['ymin']:detection['ymax'], detection['xmin']:detection['xmax']] = 0
        blur_mask[detection['ymin']:detection['ymax'], detection['xmin']:detection['xmax']] = 255

    blur_factor = (image.shape[0] + image.shape[1]) * (60 / 5000)

    original_image = image.copy()
    blurred_image = cv2.GaussianBlur(original_image, (0, 0), blur_factor)

    original_image = cv2.bitwise_and(original_image, original_image, mask=image_mask)
    blurred_image = cv2.bitwise_and(blurred_image, blurred_image, mask=blur_mask)

    return cv2.bitwise_or(original_image, blurred_image)
