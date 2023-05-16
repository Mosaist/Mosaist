import cv2
import torch

import util.image_util as image_util
import util.path_util as path_util
import util.video_util as video_util
import util.detection_util as detection_util

from mosaic.sieve import Sieve

class Recognizer:
    default_model_path = path_util.model_path('widerface-yolov5n')

    def __init__(self, model_path=default_model_path):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', model_path)
        self.sieve = Sieve(self)

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
                    'conf': conf
                } for xmin, ymin, xmax, ymax, cls, name, conf in zip(result['xmin'], result['ymin'], result['xmax'], result['ymax'], result['class'], result['name'], result['confidence'])
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

    def process_images(self, images, fun, do_sieve=True, do_split=True, rows=2, cols=2, split_rect=False):
        detections = self.images_to_detections(images)

        if do_split:
            splited_images = [image_util.split_image(image, rows, cols, split_rect) for image in images]

            detections_split = []
            for splited in splited_images:
                splited_height, splited_width = splited[0][0].shape[:2]
                detection = []

                for r, row in enumerate(splited):
                    for c, row_detection in enumerate(self.images_to_detections(row)):
                        for det in row_detection:
                            det['xmin'] += c * splited_width
                            det['xmax'] += c * splited_width
                            det['ymin'] += r * splited_height
                            det['ymax'] += r * splited_height
                        detection.extend(row_detection)

                detections_split.append(detection)

            for i in range(len(detections)):
                detections[i].extend(detections_split[i])
        detections = detection_util.apply_detections_nms(detections, iou_criteria=0)

        result = []
        for image_, detection in zip(images, detections):
            image = image_.copy()

            for det in detection:
                if do_sieve:
                    if self.sieve.is_allowed(image_util.face_cut(image, det)):
                        continue
                image = fun(image, det)

            result.append(image)

        return result

    def process_video(self, video_name, fun, do_sieve=True, do_split=True, rows=2, cols=2, split_rect=False):
        video_path = path_util.input_video_path(video_name)
        video = cv2.VideoCapture(video_path)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        size = video_util.get_size(video)
        fps = video_util.get_fps(video)
        frame_count = video_util.get_frame_count(video)
        path = path_util.output_video_path(video_name)

        out = cv2.VideoWriter(path, fourcc, fps, size)
        index = 0
        for image in video_util.get_images(video):
            print(f'[Video processing] {video_name} | {index / frame_count * 100}')
            image = fun(image, do_sieve, do_split, rows, cols, split_rect)
            out.write(image)
            index += 1
        out.release()

        video_util.to_h264(video_name)

        return path

    def rect_images_fun(self, image, det):
        return cv2.rectangle(image, (det['xmin'], det['ymin']), (det['xmax'], det['ymax']), (0, 255, 0), 3)

    def mosaic_images_fun(self, image, det):
        temp = image[det['ymin']:det['ymax'], det['xmin']:det['xmax']]
        temp = image_util.pixelate(temp)
        image[det['ymin']:det['ymax'], det['xmin']:det['xmax']] = temp

        return image

    def rect_video_fun(self, image, do_sieve=True, do_split=True, rows=2, cols=2, split_rect=False):
        return self.rect_images([image], do_sieve, do_split, rows, cols, split_rect)[0]

    def mosaic_video_fun(self, image, do_sieve=True, do_split=True, rows=2, cols=2, split_rect=False):
        return self.mosaic_images([image], do_sieve, do_split, rows, cols, split_rect)[0]

    def rect_images(self, images, do_sieve=True, do_split=True, rows=2, cols=2, split_rect=False):
        return self.process_images(images, self.rect_images_fun, do_sieve, do_split, rows, cols, split_rect)

    def mosaic_images(self, images, do_sieve=True, do_split=True, rows=2, cols=2, split_rect=False):
        return self.process_images(images, self.mosaic_images_fun, do_sieve, do_split, rows, cols, split_rect)

    def rect_video(self, video_name, do_sieve=True, do_split=True, rows=2, cols=2, split_rect=False):
        return self.process_video(video_name, self.rect_video_fun, do_sieve, do_split, rows, cols, split_rect)

    def mosaic_video(self, video_name, do_sieve=True, do_split=True, rows=2, cols=2, split_rect=False):
        return self.process_video(video_name, self.mosaic_video_fun, do_sieve, do_split, rows, cols, split_rect)