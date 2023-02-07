import json
import base64
import datetime

import asyncio
import cv2
import ssl
import numpy as np
import websockets

from facial_stuffs import *
from image_stuffs import *
from video_stuffs import *

config = json.load(open(f'../../config.json'))

f = FaceRecognizer()
"""
얼굴 인식 관련 모델
"""

async def socket_root(websocket):
    """
    웹소켓 서버 루트

    Params:
        websocket: 웹소켓 인스턴스.
    """

    async for message in websocket:
        method, content = message.split('::')
        response = 'false'

        print(f'{datetime.datetime.now()} [{method}] {content[:20]}')

        try:
            if method == 'image-mosaic':
                response = socket_mosaic_image(content)
            elif method == 'video-mosaic':
                pass
            else:
                pass
        except:
            pass

        await websocket.send(response)

def socket_mosaic_image(content):
    """
    웹소켓에 대응하는 이미지 모자이크

    Params:
        content: 웹소켓으로 전송 받은 이미지 파일.

    Returns:
        변환된 이미지.
    """

    encoded_image = np.frombuffer(base64.b64decode(content), np.uint8)
    image = cv2.imdecode(encoded_image, cv2.IMREAD_COLOR)

    detections = f.image_to_detections(image)
    image = mosaic_image(image, detections[0])

    return cv2.imencode('.png', image)[1].tobytes()

async def main():
    print(f' * Running on wss://{config["server"]["ip"]}:{config["server"]["back"]["socketPort"]}')

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=config['server']['sslCert'], keyfile=config['server']['sslKey'])

    async with websockets.serve(socket_root, config['server']['ip'], config['server']['back']['socketPort'], ssl=ssl_context, max_size=10000000):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())