import ssl

from flask import Flask, request, send_file
from flask_cors import CORS

import util.request_util as request_util
import util.image_util as image_util
import util.response_util as response_util
import util.video_util as video_util

from util.config_util import CONFIG
from util.exception_util import ColorSpaceNotSupported
from util.response_util import ResponseCode
from mosaic.recognizer import Recognizer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = CONFIG.path.inputPath

CORS(app)

rec = Recognizer()

@app.route('/image/rect', methods=['POST'])
def image_rect_post():
    if 'file' not in request.files:
        return ResponseCode.BAD_REQUEST('File not found')
    file = request.files['file']

    if not request_util.is_allowed_image_format(file.filename):
        return ResponseCode.BAD_REQUEST('File not found or format not allowed')

    image = image_util.from_file(file)
    image = rec.rect_images([image], do_sieve=False)[0]

    return response_util.response_image(image)

@app.route('/video/rect', methods=['POST'])
def video_rect_post():
    if 'file' not in request.files:
        return ResponseCode.BAD_REQUEST('File not found')
    file = request.files['file']

    if not request_util.is_allowed_video_format(file.filename):
        return ResponseCode.BAD_REQUEST('File not found or format not allowed')

    video_util.save_from_file(file)
    video_path = rec.rect_video(file.filename, do_sieve=False)

    return send_file(video_path, 'video/mp4')

@app.route('/image/mosaic', methods=['POST'])
def image_mosaic_post():
    if 'file' not in request.files:
        return ResponseCode.BAD_REQUEST('File not found')
    file = request.files['file']

    if not request_util.is_allowed_image_format(file.filename):
        return ResponseCode.BAD_REQUEST('File not found or format not allowed')

    image = image_util.from_file(file)
    image = rec.rect_images([image], do_sieve=False)[0]

    return response_util.response_image(image)

@app.route('/video/mosaic', methods=['POST'])
def video_mosaic_post():
    if 'file' not in request.files:
        return ResponseCode.BAD_REQUEST('File not found')
    file = request.files['file']

    if not request_util.is_allowed_video_format(file.filename):
        return ResponseCode.BAD_REQUEST('File not found or format not allowed')

    video_util.save_from_file(file)
    video_path = rec.rect_video(file.filename, do_sieve=False)

    return send_file(video_path, 'video/mp4')

@app.route('/image/targetset', methods=['POST'])
def image_targetset_post():
    return ResponseCode.NOT_IMPLEMENTED()

@app.route('/video/targetset', methods=['POST'])
def video_targetset_post():
    return ResponseCode.NOT_IMPLEMENTED()

def main():
    if CONFIG.server.useProxy:
        app.run(host='127.0.0.1', port=CONFIG.server.back.httpPort)
    else:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=CONFIG.server.sslCert, keyfile=CONFIG.server.sslKey)
        app.run(host=CONFIG.server.ip, port=CONFIG.server.back.httpPort, ssl_context=ssl_context)

if __name__ == '__main__':
    main()