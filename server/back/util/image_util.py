import base64

import cv2
import numpy as np

from util.exception_util import ColorSpaceNotSupported

def from_file(file):
    file_byte = np.fromfile(file, np.uint8)
    image = cv2.imdecode(file_byte, cv2.IMREAD_UNCHANGED)
    return image

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