import os
import json
import traceback

import cv2
import ssl
import numpy as np

from flask import Flask, request, send_file, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename

from facial_stuffs import *
from image_stuffs import *
from video_stuffs import *
from model_stuffs import *

config = json.load(open(f'{os.path.dirname(__file__)}/../../config.json'))
"""
전역 환경 변수 모음
"""

app = Flask(__name__)
"""
플라스크 HTTP 서버 인스턴스
"""
app.config['UPLOAD_FOLDER'] = config['path']['inputPath']
"""
입력 파일에 대한 경로 설정
"""

CORS(app)

f = FaceRecognizer()
"""
얼굴 인식 관련 모델
"""

def _allowed_image_file(filename):
    """
    이미지 파일에 대한 포맷 확인

    Params:
        filename: 확인할 대상 이미지 파일 이름.

    Returns:
        파일 이름의 유효성.

    """

    return '.' in filename and filename.rsplit('.', 1)[1] in config['server']['back']['allowedImageExtensions']

def _allowed_video_file(filename):
    """
    동영상 파일에 대한 포맷 확인

    Params:
        filename: 확인할 대상 동영상 파일 이름.

    Returns:
        파일 이름의 유효성.

    """

    return '.' in filename and filename.rsplit('.', 1)[1] in config['server']['back']['allowedVideoExtensions']

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

    if not _allowed_image_file(file.filename):
        return 'false'

    file_bytes = np.fromfile(file, np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)

    detections = f.image_to_detections(image)
    image = mosaic_image(image, detections[0], f)

    response = make_response(cv2.imencode('.png', image)[1].tobytes())
    response.headers.set('Content-Type', 'image/png')

    return response

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

    if not _allowed_video_file(file.filename):
        return 'false'

    filename = secure_filename(file.filename)
    file.save(f'{config["path"]["inputPath"]}/videos/{filename}')

    video = cv2.VideoCapture(str(f'{config["path"]["inputPath"]}/videos/{filename}'))
    images = video_to_images(video)

    detections = f.image_to_detections(images)
    images = [mosaic_image(image, detection, f) for image, detection in zip(images, detections)]
    save_images_as_video(images, f'{config["path"]["outputPath"]}/videos/{config["server"]["back"]["editPrefix"]}_{filename}', get_fps(video))

    return send_file(f'{config["path"]["outputPath"]}/videos/{config["server"]["back"]["editPrefix"]}_{filename}', mimetype='video/mp4')

@app.route('/video/training', methods=['POST'])
def video_training_post():
    """
    입력된 동영상 파일을 사진으로 변환하여 학습

    Returns:
        학습 성공 여부.
    """

    if 'file' not in request.files:
        return 'false'
    file = request.files['file']

    if file.filename == '':
        return 'false'

    if not _allowed_video_file(file.filename):
        return 'false'

    filename = secure_filename(file.filename)
    file.save(f'{config["path"]["inputPath"]}/videos/{filename}')

    dataset_prefix = 'custom_'
    dataset_index = 0
    while os.path.exists(f'{config["path"]["datasetPath"]}/{dataset_prefix}{dataset_index}'):
        dataset_index += 1

    dataset_name = f'{dataset_prefix}{dataset_index}'

    print(f'[Custom Model Training]: {dataset_name}')

    try:
        print('[Custom Model Training]: Convert video into dataset.')
        video_to_dataset(f'{filename}', dataset_name, f, True)

        print('[Custom Model Training]: Train model.')
        train_images(dataset_name)

        print('[Custom Model Training]: Set model.')
        f.set_model(f'{config["path"]["modelPath"]}/{dataset_name}/weights/best.pt')
    except Exception:
        print('[Custom Model Training]: An exception has occured.')
        print(traceback.format_exc())
        return 'false'

    return 'true'

@app.route('/video/targetset', methods=['POST'])
def video_targetset_post():
    if 'file' not in request.files:
        return 'false'
    file = request.files['file']

    if file.filename == '':
        return 'false'

    if not _allowed_video_file(file.filename):
        return 'false'

    filename = secure_filename(file.filename)
    file.save(f'{config["path"]["inputPath"]}/videos/{filename}')

    try:
        print('[Custom Targetset]: Convert video into targetset.')
        video_to_targetset(f'{filename}', f, True)
    except Exception:
        print('[Custom Targetset]: An exception has occured.')
        print(traceback.format_exc())
        return 'false'

    return 'true'

def main():
    if config['server']['useProxy']:
        app.run(host='127.0.0.1', port=config['server']['back']['httpPort'])
    else:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=config['server']['sslCert'], keyfile=config['server']['sslKey'])

        app.run(host=config['server']['ip'], port=config['server']['back']['httpPort'], ssl_context=ssl_context)

if __name__ == '__main__':
    main()