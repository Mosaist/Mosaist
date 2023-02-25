import cv2

import util.image_util as image_util

from util.config_util import CONFIG

def save_from_file(file):
    file_name = file.filename
    file_path = f'{CONFIG.path.inputPath}/videos/{file_name}'
    file.save(file_path)

    return file_path

def get_images(video):
    success, image = video.read()

    while success:
        success, image = video.read()
        if not success:
            break

        yield image

def get_size(video):
    major_ver, _, _ = (cv2.__version__).split('.')
 
    if int(major_ver) < 3 :
        return tuple(map(int, (
            video.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH),
            video.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        )))
    else :
        return tuple(map(int, (
            video.get(cv2.CAP_PROP_FRAME_WIDTH),
            video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )))

def get_fps(video):
    major_ver, _, _ = (cv2.__version__).split('.')
 
    if int(major_ver) < 3 :
        return video.get(cv2.cv.CV_CAP_PROP_FPS)
    else :
        return video.get(cv2.CAP_PROP_FPS)