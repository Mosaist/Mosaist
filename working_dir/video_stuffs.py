import cv2
import numpy as np

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

def save_images_as_video(images: list, path: str, fps: int=30) -> cv2.VideoWriter:
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
