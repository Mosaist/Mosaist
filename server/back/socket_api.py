import datetime
import ssl
import asyncio
import websockets

import cv2
import numpy as np

import util.image_util as image_util

from mosaic.recognizer import Recognizer
from util.config_util import CONFIG

rec = Recognizer()
temp_storage = { }

async def socket_root(websocket):
    async for message in websocket:
        method, content = message.split('::')
        response = 'false'

        print(f'{datetime.datetime.now()} [{method}] {content[:20]}')

        try:
            if method == 'image-rect':
                response = socket_image_rect(content, websocket.id)
            elif method == 'image-mosaic':
                response = socket_image_mosaic(content, websocket.id)
            else:
                response = 'Method not found'
        except:
            response = 'Internal server error'

        await websocket.send(response)

def socket_image_rect(content, id):
    image = image_util.from_socket(content)
    image = rec.rect_images([image], do_sieve=False)[0][0]

    return image_util.to_png_byte(image)

def socket_image_mosaic(content, id):
    if id not in temp_storage:
        temp_storage[id] = { }
        temp_storage[id]['index'] = 0
        temp_storage[id]['prev_image'] = None
        temp_storage[id]['prev_corners'] = None
        temp_storage[id]['prev_windows'] = None

    image = image_util.from_socket(content)
    image_temp = image.copy()

    if temp_storage[id]['index'] % 10 == 0:
        image, detections = rec.rect_images([image], do_sieve=False)
        image = image[0]
        temp_storage[id]['prev_corners'] = [[det['xmin'], det['ymin']] for det in detections[0]]
        temp_storage[id]['prev_windows'] = [[det['xmax'] - det['xmin'], det['ymax'] - det['ymin']] for det in detections[0]]
    elif len(temp_storage[id]['prev_corners']) > 0:
        current_corners, _, _ = cv2.calcOpticalFlowPyrLK(temp_storage[id]['prev_image'], image, np.array(temp_storage[id]['prev_corners'], dtype=np.float32), None)
        temp_storage[id]['prev_corners'] = current_corners

        for corner, window in zip(current_corners, temp_storage[id]['prev_windows']):
            corner = tuple(map(int, corner))
            cv2.rectangle(image, corner, (corner[0] + window[0], corner[1] + window[1]), (255, 0, 0), 3)

    temp_storage[id]['prev_image'] = image_temp
    temp_storage[id]['index'] += 1

    return image_util.to_png_byte(image)

async def main():
    print(f' * Running on wss://{CONFIG.server.ip}:{CONFIG.server.back.socketPort}')

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=CONFIG.server.sslCert, keyfile=CONFIG.server.sslKey)

    async with websockets.serve(socket_root, CONFIG.server.ip, CONFIG.server.back.socketPort, ssl=ssl_context, max_size=10000000):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
