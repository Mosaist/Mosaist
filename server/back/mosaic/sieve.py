import os

import cv2
from  deepface import DeepFace
from deepface.commons import distance as dst

import util.image_util as image_util
import util.path_util as path_util

class Sieve:
    default_model_name = 'Facenet'
    default_metric = 'euclidean_l2'
    default_targetset_name = ''
    allowed_face_embeddings = []

    def __init__(self, rec, targetset_name=default_targetset_name):
        allowed_images_path = path_util.targetset_path(targetset_name)
        allowed_images_names = os.listdir(allowed_images_path)
        allowed_images = [cv2.imread(f'{allowed_images_path}/{image_name}', cv2.IMREAD_UNCHANGED) for image_name in allowed_images_names]

        detections = rec.images_to_detections(allowed_images)

        result = []
        for image_, detection in zip(allowed_images, detections):
            for det in detection:
                image = image_util.face_cut(image_, det)
                result.append(image)

        for image in result:
            Sieve.allowed_face_embeddings += DeepFace.represent(image, model_name=Sieve.default_model_name, enforce_detection=False)

    def verify_embedding(
        self,
        embed1,
        embed2,
        model_name="VGG-Face",
        detector_backend="opencv",
        distance_metric="cosine",
    ):
        rep1 = embed1['embedding']
        rep2 = embed2['embedding']

        if distance_metric == "cosine":
            distance = dst.findCosineDistance(rep1, rep2)
        elif distance_metric == "euclidean":
            distance = dst.findEuclideanDistance(rep1, rep2)
        elif distance_metric == "euclidean_l2":
            distance = dst.findEuclideanDistance(
                dst.l2_normalize(rep1), dst.l2_normalize(rep2)
            )
        else:
            raise ValueError("Invalid distance_metric passed - ", distance_metric)

        threshold = dst.findThreshold(model_name, distance_metric)

        resp_obj = {
            "verified": distance <= threshold,
            "distance": distance,
            "threshold": threshold,
            "model": model_name,
            "detector_backend": detector_backend,
            "similarity_metric": distance_metric,
        }

        return resp_obj

    def is_allowed(self, face):
        temp = DeepFace.represent(face, model_name=Sieve.default_model_name, enforce_detection=False)
        if not temp:
            return False

        face_embedding = temp[0]

        for allowed_embedding in Sieve.allowed_face_embeddings:
            res = self.verify_embedding(face_embedding, allowed_embedding, model_name=Sieve.default_model_name, distance_metric=Sieve.default_metric)

            if res['verified']:
                return True

        return False