import cv2
import numpy as np

def from_file(file):
    file_byte = np.fromfile(file, np.uint8)
    return cv2.imdecode(file_byte, cv2.IMREAD_UNCHANGED)

def to_png_byte(image):
    return cv2.imencode('.png', image)[1].tobytes()