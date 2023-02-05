import cv2
import numpy as np
import ssl

from flask import Flask, request, send_file, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename

from facial_stuffs import *
from image_stuffs import *
from video_stuffs import *
from model_stuffs import *

from config import *

app = Flask(__name__)
"""
플라스크 HTTP 서버 인스턴스
"""
app.config['UPLOAD_FOLDER'] = INPUT_PATH

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

    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_IMAGE_EXTENSIONS

def _allowed_video_file(filename):
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
    """
    메인 페이지

    Returns:
        메인 페이지 HTML
    """

    return """<!DOCTYPE html>
<html lang="ko">
    <head>
        <meta charset="UTF-8" />
        <title>Mosaist</title>
        <style>
            h1 { text-align: center; }
            h4 { text-align: center; }
            main {
                width: 800px;
                margin: 0 auto;
            }

            .center {
                display: grid;
                place-items: center;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Mosaist</h1>
        </header>
        <hr>
        <main>
            <section>
                <h3>[POST] /image/mosaic</h3>
                <div class="center">
                    <p>
                        body {<br>
                        &nbsp;&nbsp;&nbsp;&nbsp;"file": "{your_image_file_here}"<br>
                        }<br>
                    </p>
                    <p>.jpg, .png are allowed.</p>
                </div>
            </section>
            <section>
                <h3>[POST] /video/mosaic</h3>
                <div class="center">
                    <p>
                        body {<br>
                        &nbsp;&nbsp;&nbsp;&nbsp"file": "{your_video_file_here}"<br>
                        }<br>
                    </p>
                    <p>.mp4 is allowed.</p>
                </div>
            </section>
        </main>
        <hr>
        <footer>
            <h4><a href="https://github.com/Mosaist/Mosaist">github</a></h4>
        </footer>
    </body>
</html>"""

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
    image = mosaic_image(image, detections[0])

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
    file.save(f'{INPUT_PATH}/videos/{filename}')

    video = cv2.VideoCapture(str(f'{INPUT_PATH}/videos/{filename}'))
    images = video_to_images(video)

    detections = f.image_to_detections(images)
    images = [mosaic_image(image, detection) for image, detection in zip(images, detections)]
    save_images_as_video(images, f'{OUTPUT_PATH}/videos/{EDIT_PREFIX}_{filename}', get_fps(video))

    return send_file(f'{OUTPUT_PATH}/videos/{EDIT_PREFIX}_{filename}', mimetype='video/mp4')

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
    file.save(f'{INPUT_PATH}/videos/{filename}')

    dataset_prefix = 'custom_'
    dataset_index = 0
    while os.path.exists(f'{DATASET_PATH}/{dataset_prefix}{dataset_index}'):
        dataset_index += 1

    dataset_name = f'{dataset_prefix}{dataset_index}'

    print(f'[Custom Model Training]: {dataset_name}')

    try:
        video_to_dataset(f'{filename}', dataset_name)
        train_images(dataset_name)

        f.set_model(f'{MODEL_PATH}/{dataset_name}/weights/best.pt')
    except Exception:
        print(Exception)
        return 'false'

    return 'true'

def main():
    print_config()

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=SSL_CERT, keyfile=SSL_KEY)

    app.run(host=IP, port=PORT, ssl_context=ssl_context)

if __name__ == '__main__':
    main()