import json
import ssl
import requests
from flask import Flask, request, Response

app = Flask(__name__)
config = json.load(open(f'../config.json'))

def _proxy(p, q):
    resp = requests.request(
        method=request.method,
        url=request.url.replace(p, q),
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
    return _proxy(config['server']['url'], f"http://localhost:{config['server']['front']['port']}")

@app.route('/front')
def front_root():
    return _proxy(config['server']['front']['url'], f"http://localhost:{config['server']['front']['port']}")

@app.route('/front/<path:path>')
def front(path):
    return _proxy(config['server']['front']['url'], f"http://localhost:{config['server']['front']['port']}")

@app.route('/back')
def back_root():
    return _proxy(config['server']['back']['httpUrl'], f"http://localhost:{config['server']['back']['httpPort']}")

@app.route('/back/<path:path>', methods=['POST'])
def back(path):
    return _proxy(config['server']['back']['httpUrl'], f"http://localhost:{config['server']['back']['httpPort']}")

def main():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=config['server']['sslCert'], keyfile=config['server']['sslKey'])

    app.run(host=config['server']['ip'], port=config['server']['port'], ssl_context=ssl_context)

if __name__ == '__main__':
    main()