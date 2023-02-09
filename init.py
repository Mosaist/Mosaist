import os
import json

PREFIX = os.path.dirname(__file__)
config = json.load(open(f'{PREFIX}/config.json'))

for key, value in config['path'].items():
    if not os.path.exists(value):
        if key == 'yoloPath':
            print('Clone YOLOv5 git repository:', value)
            os.system(f'git clone https://github.com/ultralytics/yolov5 {value}')
        elif key == 'inputPath' or key == 'outputPath':
            print('Create directory:', f'{value}/images')
            print('Create directory:', f'{value}/videos')
            os.makedirs(f'{value}/images')
            os.makedirs(f'{value}/videos')
        else:
            print('Create directory:', value)
            os.makedirs(value)
    else:
        print('Directory exists:', value)
