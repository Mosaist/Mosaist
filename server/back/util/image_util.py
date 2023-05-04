import base64

import cv2
import numpy as np

from util.exception_util import ColorSpaceNotSupported

def from_file(file):
    file_byte = np.fromfile(file, np.uint8)
    image = cv2.imdecode(file_byte, cv2.IMREAD_UNCHANGED)
    return to_bgr(to_rgb(image))

def from_socket(content):
    encoded_image = np.frombuffer(base64.b64decode(content), np.uint8)
    image = cv2.imdecode(encoded_image, cv2.IMREAD_COLOR)
    return image

def to_rgb(image):
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
    else:
        raise ColorSpaceNotSupported()

    return image

def to_bgr(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

def to_png_byte(image):
    return cv2.imencode('.png', image)[1].tobytes()

def face_cut(image, det):
    return image[det['ymin']:det['ymax'], det['xmin']:det['xmax']]

def pixelate(image):
    height, width, _ = image.shape

    temp = cv2.resize(image, (8, 8), interpolation=cv2.INTER_LINEAR)

    return cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

def split_image(image, rows=2, cols=2, debug=False):
    height, width = image.shape[:2]     # 원본 사진 크기.

    # 균등하게 나눠질 수 있도록 패딩 추가.
    while image.shape[0] % rows != 0:
        image = np.vstack((image, [image[-1]]))
    while image.shape[1] % cols != 0:
        image = np.hstack((image, image[:, -1].reshape(image.shape[0], 1, image.shape[2])))

    # 이미지 분할. (rows * cols의 영역으로 분할.)
    images = np.vsplit(image, rows)
    images = list(map(lambda section: np.hsplit(section, cols), images))

    # 디버그 옵션 추가 시 분할선 추가.
    if debug:
        for imgs in images:
            for img in imgs:
                img = cv2.rectangle(img, (0, 0), list(map(lambda e: e - 3, reversed(img.shape[:2]))), (0, 255, 0), 3)

    # 원본 사진 크기 복구.
    while image.shape[0] != height:
        image = np.delete(image, -1, axis=0)
    while image.shape[1] != width:
        image = np.delete(image, -1, axis=1)

    return images

def merge_images(images):
    temp = [np.hstack(image_row) for image_row in images]
    return np.vstack(temp)