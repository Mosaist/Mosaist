import json
from flask import Flask, render_template, send_file

config = json.load(open(f'../../config.json'))

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
    app.run(host='127.0.0.1', port=config['server']['front']['port'])
