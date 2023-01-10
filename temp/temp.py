import ssl
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/<url>')
def map(url):
    return render_template(url)

if __name__ == '__main__':
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile='', keyfile='')
    app.run(host='0.0.0.0', port=443, ssl_context=ssl_context)
