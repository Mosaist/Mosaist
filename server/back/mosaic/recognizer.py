import os

import cv2
import ffmpeg
import torch

import util.image_util as image_util
import util.video_util as video_util

from util.config_util import CONFIG

class FaceRecognizer:
    default_model_path = f'{CONFIG.path.modelPath}/widerface-yolov5n/weights/best.pt'

    def __init__(self, model_path=default_model_path):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', model_path)

    def set_model(self, model_path):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', model_path)

    def images_to_detections(self, images):
        return [
            [
                {
                    'xmin': int(xmin),
                    'ymin': int(ymin),
                    'xmax': int(xmax),
                    'ymax': int(ymax),
                    'class': cls,
                    'name': name,
                } for xmin, ymin, xmax, ymax, cls, name in zip(result['xmin'], result['ymin'], result['xmax'], result['ymax'], result['class'], result['name'])
            ] for result in self.model(images).pandas().xyxy
        ]

    def images_to_labels(self, images):
        return [
            [
                [
                    cls,
                    (int(xmin) + int(xmax)) / 2 / width,
                    (int(ymin) + int(ymax)) / 2 / height,
                    (int(xmax) - int(xmin)) / width,
                    (int(ymax) - int(ymin)) / height
                ] for width, height, xmin, ymin, xmax, ymax, cls
                  in zip([images.shape[1]] * len(result['xmin']), [images.shape[0]] * len(result['xmin']), result['xmin'], result['ymin'], result['xmax'], result['ymax'], result['class'])
            ] for images, result in zip(images, self.model(images).pandas().xyxy)
        ]

    def rect_images(self, images):
        detections = self.images_to_detections(images)

        result = []
        for image_, detection in zip(images, detections):
            image = image_.copy()

            for det in detection:
                image = cv2.rectangle(image, (det['xmin'], det['ymin']), (det['xmax'], det['ymax']), (0, 255, 0), 3)

            result.append(image)

        return result

    def rect_video(self, video_name):
        video = cv2.VideoCapture(f'{CONFIG.path.inputPath}/videos/{video_name}')

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        size = video_util.get_size(video)
        fps = video_util.get_fps(video)
        path = f'{CONFIG.path.outputPath}/videos/{video_name}'

        out = cv2.VideoWriter(path, fourcc, fps, size)
        for image in video_util.get_images(video):
            image = self.rect_images([image])[0]
            out.write(image)
        out.release()

        os.rename(path, f'{path}.temp')
        ffmpeg.input(f'{path}.temp').output(path, vcodec='libx264').run()
        os.remove(f'{path}.temp')

        return path

    def mosaic_images(self, images):
        detections = self.images_to_detections(images)

        result = []
        for image_, detection in zip(images, detections):
            image = image_.copy()

            for det in detection:
                temp = image[det['ymin']:det['ymax'], det['xmin']:det['xmax']]
                temp = image_util.pixelate(temp)
                image[det['ymin']:det['ymax'], det['xmin']:det['xmax']] = temp

            result.append(image)

        return result

    def mosaic_video(self, video_name):
        video = cv2.VideoCapture(f'{CONFIG.path.inputPath}/videos/{video_name}')

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        size = video_util.get_size(video)
        fps = video_util.get_fps(video)
        path = f'{CONFIG.path.outputPath}/videos/{video_name}'

        out = cv2.VideoWriter(path, fourcc, fps, size)
        for image in video_util.get_images(video):
            image = self.mosaic_images([image])[0]
            out.write(image)
        out.release()

        os.rename(path, f'{path}.temp')
        ffmpeg.input(f'{path}.temp').output(path, vcodec='libx264').run()
        os.remove(f'{path}.temp')

        return path