import datetime
import ssl
import asyncio

import websockets

import util.image_util as image_util

from mosaic.recognizer import Recognizer
from util.config_util import CONFIG

rec = Recognizer()

async def socket_root(websocket):
    async for message in websocket:
        method, content = message.split('::')
        response = 'false'

        print(f'{datetime.datetime.now()} [{method}] {content[:20]}')

        try:
            if method == 'image-rect':
                response = socket_image_rect(content)
            elif method == 'image-mosaic':
                response = socket_image_mosaic(content)
            else:
                response = 'Method not found'
        except:
            response = 'Internal server error'

        await websocket.send(response)

def socket_image_rect(content):
    image = image_util.from_socket(content)
    image = rec.rect_images([image], do_sieve=False)[0][0]

    return image_util.to_png_byte(image)

def socket_image_mosaic(content):
    image = image_util.from_socket(content)
    image = rec.rect_images([image], do_sieve=False)[0][0]

    return image_util.to_png_byte(image)

async def main():
    print(f' * Running on wss://{CONFIG.server.ip}:{CONFIG.server.back.socketPort}')

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=CONFIG.server.sslCert, keyfile=CONFIG.server.sslKey)

    async with websockets.serve(socket_root, CONFIG.server.ip, CONFIG.server.back.socketPort, ssl=ssl_context, max_size=10000000):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
