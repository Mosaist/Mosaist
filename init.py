import os
import json

PREFIX = os.path.dirname(__file__)
config = json.load(open(f'{PREFIX}/config.json'))

print('[Info] Initiate paths...')
for key, value in config['path'].items():
    if not os.path.exists(value):
        if key == 'yoloPath':
            print('[Fatal] yolo does not exist. Please run "pip install -r requirements.txt" first.')
            break
        if key == 'inputPath' or key == 'outputPath':
            print('[Info] Create directory:', f'{value}/images')
            print('[Info] Create directory:', f'{value}/videos')
            os.makedirs(f'{value}/images')
            os.makedirs(f'{value}/videos')
        else:
            print('[Info] Create directory:', value)
            os.makedirs(value)
    else:
        print('[Info] Directory already exists:', value)
print('[Info] Done')