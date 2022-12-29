import cv2
import numpy as np
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename

from facial_stuffs import *
from image_stuffs import *
from video_stuffs import *

from config import *

ALLOWED_IMAGE_EXTENSIONS = set(['jpg', 'png', 'jpeg'])
"""
허용된 이미지 형식
"""

ALLOWED_VIDEO_EXTENSIONS = set(['mp4'])
"""
허용된 동영상 형식
"""

EDIT_PREFIX = 'edited_'
"""
출력 디렉토리에 저장될 파일의 접두어
"""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = INPUT_DIR

f = FaceRecognizer()

def allowed_image_file(filename):
    """
    이미지 파일에 대한 포맷 확인

    Params:
        filename: 확인할 대상 이미지 파일 이름.

    Returns:
        파일 이름의 유효성.

    """

    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_IMAGE_EXTENSIONS

def allowed_video_file(filename):
    """
    동영상 파일에 대한 포맷 확인

    Params:
        filename: 확인할 대상 동영상 파일 이름.

    Returns:
        파일 이름의 유효성.

    """

    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_VIDEO_EXTENSIONS

@app.route('/')
def home():
    return 'Hello, world!'

@app.route('/image/mosaic', methods=['GET'])
def image_mosaic_get():
    """
    입력된 이미지 파일의 이름을 입력 폴더에서 찾아 변환 후 출력 폴더에 저장

    Returns:
        변환 성공 여부.
    """

    image_name = request.args['image']

    if not allowed_image_file(image_name):
        return 'false'

    try:
        image = cv2.imread(INPUT_DIR + image_name)
    except:
        return 'false'

    detections = f.image_to_detections(image)
    image = mosaic_image(image, detections[0])
    cv2.imwrite(OUTPUT_DIR + EDIT_PREFIX + image_name, image)

    return 'true'

@app.route('/image/mosaic', methods=['POST'])
def image_mosaic_post():
    """
    입력된 이미지 파일을 변환하여 이미지로 반환

    Returns:
        변환된 이미지 또는 성공 여부.
    """

    if 'file' not in request.files:
        return 'false'
    file = request.files['file']

    if file.filename == '':
        return 'false'

    if not allowed_image_file(file.filename):
        return 'false'

    filename = secure_filename(file.filename)
    file_bytes = np.fromfile(file, np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)

    detections = f.image_to_detections(image)
    image = mosaic_image(image, detections[0])
    cv2.imwrite(OUTPUT_DIR + EDIT_PREFIX + filename, image)

    return send_file(OUTPUT_DIR + EDIT_PREFIX + filename, mimetype='image/png')

@app.route('/video/mosaic', methods=['GET'])
def video_mosaic_get():
    """
    입력된 동영상 파일의 이름을 입력 폴더에서 찾아 변환 후 출력 폴더에 저장

    Returns:
        변환 성공 여부.
    """

    video_name = request.args['video']

    if not allowed_video_file(video_name):
        return 'false'

    try:
        video = cv2.VideoCapture(INPUT_DIR + video_name)
    except:
        return 'false'

    images = video_to_images(video)

    detections = f.image_to_detections(images)
    images = [mosaic_image(image, detection) for image, detection in zip(images, detections)]
    save_images_as_video(images, OUTPUT_DIR + EDIT_PREFIX + video_name, get_fps(video))

    return 'true'

@app.route('/video/mosaic', methods=['POST'])
def video_mosaic_post():
    """
    입력된 동영상 파일을 변환하여 동영상으로 반환

    Returns:
        변환된 동영상 또는 성공 여부.
    """

    if 'file' not in request.files:
        return 'false'
    file = request.files['file']

    if file.filename == '':
        return 'false'

    if not allowed_video_file(file.filename):
        return 'false'

    filename = secure_filename(file.filename)
    file.save(INPUT_DIR + filename)

    video = cv2.VideoCapture(str(INPUT_DIR + filename))
    images = video_to_images(video)

    detections = f.image_to_detections(images)
    images = [mosaic_image(image, detection) for image, detection in zip(images, detections)]
    save_images_as_video(images, OUTPUT_DIR + EDIT_PREFIX + filename, get_fps(video))

    return send_file(OUTPUT_DIR + EDIT_PREFIX + filename, mimetype='image/mp4')

if __name__ == '__main__':
    app.run(port=PORT)