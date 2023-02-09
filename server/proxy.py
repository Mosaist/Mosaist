import os
import json
import ssl
import requests
from flask import Flask, request, Response

config = json.load(open(f'{os.path.dirname(__file__)}/../config.json'))
"""
전역 환경 변수 모음
"""

app = Flask(__name__)
"""
플라스크 프록시 서버 인스턴스
"""

def _proxy(req_url, dest_url):
    """
    *내부 함수

    프록시 요청에 대한 url을 목적지 url에 대한 요청으로 변환

    Params:
        req_url: 프록시 서버에 대한 url.
        dest_url: 목적지 서버에 대한 url.

    Returns:
        프록시 요청에 대한 응답.
    """

    resp = requests.request(
        method=request.method,
        url=request.url.replace(req_url, dest_url),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)

    return response

@app.route('/')
def root():
    """
    최상위 도메인에 대한 프록시 처리

    Returns:
        대응하는 프록시 응답.
    """

    return _proxy(config['server']['url'], f"http://localhost:{config['server']['front']['port']}")

@app.route('/front')
def front_root():
    """
    프론트에 대한 프록시 처리

    Returns:
        대응하는 프록시 응답.
    """

    return _proxy(config['server']['front']['url'], f"http://localhost:{config['server']['front']['port']}")

@app.route('/front/<path:path>')
def front(path):
    """
    프론트에 대한 프록시 처리

    Params:
        path: 프록시 서버에 대한 url.

    Returns:
        대응하는 프록시 응답.
    """

    return _proxy(config['server']['front']['url'], f"http://localhost:{config['server']['front']['port']}")

@app.route('/back')
def back_root():
    """
    백에 대한 프록시 처리

    Returns:
        대응하는 프록시 응답.
    """

    return _proxy(config['server']['back']['httpUrl'], f"http://localhost:{config['server']['back']['httpPort']}")

@app.route('/back/<path:path>', methods=['POST'])
def back(path):
    """
    백에 대한 프록시 처리

    Params:
        path: 프록시 서버에 대한 url.

    Returns:
        대응하는 프록시 응답.
    """

    return _proxy(config['server']['back']['httpUrl'], f"http://localhost:{config['server']['back']['httpPort']}")

def main():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=config['server']['sslCert'], keyfile=config['server']['sslKey'])

    app.run(host=config['server']['ip'], port=config['server']['port'], ssl_context=ssl_context)

if __name__ == '__main__':
    main()
