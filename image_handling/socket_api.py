import datetime
import asyncio
import websockets
import ssl
import base64
import cv2
import numpy as np

from facial_stuffs import *
from image_stuffs import *
from video_stuffs import *

from config import *

f = FaceRecognizer()

async def root(websocket):
    async for message in websocket:
        method, content = message.split('::')
        response = 'false'

        print(f'{datetime.datetime.now()} [{method}] {content[:20]}')

        try:
            if method == 'image-mosaic':
                response = _mosaic_image(content)
            elif method == 'video-mosaic':
                pass
            else:
                pass
        except:
            pass

        await websocket.send(response)

def _mosaic_image(content):
    encoded_image = np.frombuffer(base64.b64decode(content), np.uint8)
    image = cv2.imdecode(encoded_image, cv2.IMREAD_COLOR)

    detections = f.image_to_detections(image)
    image = mosaic_image(image, detections[0])

    return cv2.imencode('.png', image)[1].tobytes()

async def main():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    ssl_cert = ''
    ssl_key = ''

    ssl_context.load_cert_chain(ssl_cert, keyfile=ssl_key)

    print_config()

    async with websockets.serve(root, IP, SOCKET_PORT, ssl=ssl_context, max_size=10000000):
        await asyncio.Future()

asyncio.run(main())