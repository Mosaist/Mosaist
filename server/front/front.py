import json
from flask import Flask, render_template

config = json.load(open(f'../../config.json'))

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html', config=config)

@app.route('/<url>')
def map(url):
    return render_template(url, config=config)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=config['server']['front']['port'])
