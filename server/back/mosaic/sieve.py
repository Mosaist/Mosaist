import os

import cv2
from  deepface import DeepFace
from deepface.commons import distance as dst

import util.path_util as path_util

from util.config_util import CONFIG

class Sieve:
    default_targetset_path = CONFIG.path.targetsetPath
    allowed_face_embeddings = []

    def __init__(self, targetset_path=default_targetset_path):
        allowed_images_path = path_util.targetset_path('')
        allowed_images_names = os.listdir(allowed_images_path)
        allowed_images = [cv2.imread(f'{allowed_images_path}/{image_name}', cv2.IMREAD_UNCHANGED) for image_name in allowed_images_names]

        for image in allowed_images:
            Sieve.allowed_face_embeddings += DeepFace.represent(image, enforce_detection=False)

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
        temp = DeepFace.represent(face, enforce_detection=False)
        if not temp:
            return False

        face_embedding = DeepFace.represent(face, enforce_detection=False)[0]

        for allowed_embedding in Sieve.allowed_face_embeddings:
            if self.verify_embedding(face_embedding, allowed_embedding)['verified']:
                return True

        return False