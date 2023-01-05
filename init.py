import os
import json

PREFIX = os.path.dirname(__file__)
config = json.load(open(f'{PREFIX}/config.json'))

for key, value in config['path'].items():
    if not os.path.exists(f'{PREFIX}/{value}'):
        if key == 'yoloPath':
            print('Clone YOLOv5 git repository:', f'{PREFIX}/{value}')
            os.system(f'git clone https://github.com/ultralytics/yolov5 {PREFIX}/{value}')
        elif key == 'inputPath' or key == 'outputPath':
            print('Create directory:', f'{PREFIX}/{value}/images')
            print('Create directory:', f'{PREFIX}/{value}/videos')
            os.makedirs(f'{PREFIX}/{value}/images')
            os.makedirs(f'{PREFIX}/{value}/videos')
        else:
            print('Create directory:', f'{PREFIX}/{value}')
            os.makedirs(f'{PREFIX}/{value}')
    else:
        print('Directory exists:', f'{PREFIX}/{value}')
