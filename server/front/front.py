import os
import ssl
import json
from flask import Flask, render_template, send_file

config = json.load(open(f'{os.path.dirname(__file__)}/../../config.json'))
"""
전역 환경 변수 모음
"""

app = Flask(__name__)
"""
플라스크 프론트 서버 인스턴스
"""

@app.route('/')
def root():
    """
    최상위 도메인에 대한 응답 처리

    Returns:
        전처리된 HTML.
    """

    return render_template('html/index.html', config=config)

@app.route('/favicon.ico')
def favicon():
    print('hi')

@app.route('/<path:path>')
def template(path):
    """
    최상위 도메인에 대한 응답 처리

    Params:
        path: 요청 url.

    Returns:
        전처리된 HTML.
    """

    return render_template(f'html/{path}', config=config)

@app.route('/resource/<path:path>')
def resource(path):
    """
    리소스 요청에 대한 응답 처리

    Params:
        path: 요청 url.

    Returns:
        요청한 리소스.
    """

    return send_file(f'templates/assets/{path}')

if __name__ == '__main__':
    if config['server']['useProxy']:
        app.run(host='127.0.0.1', port=config['server']['front']['port'])
    else:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=config['server']['sslCert'], keyfile=config['server']['sslKey'])

        app.run(host=config['server']['ip'], port=config['server']['front']['port'], ssl_context=ssl_context)
