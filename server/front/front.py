import os
import ssl
import json
from flask import Flask, render_template, send_file

config = json.load(open(f'{os.path.dirname(__file__)}/../../config.json'))

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html', config=config)

@app.route('/<url>')
def template(url):
    return render_template(url, config=config)

@app.route('/resource/<url>')
def resource(url):
    return send_file(f'resources/{url}')

if __name__ == '__main__':
    if config['server']['useProxy']:
        app.run(host='127.0.0.1', port=config['server']['front']['port'])
    else:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=config['server']['sslCert'], keyfile=config['server']['sslKey'])

        app.run(host=config['server']['ip'], port=config['server']['front']['port'], ssl_context=ssl_context)
