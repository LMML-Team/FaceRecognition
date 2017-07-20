import skimage.io as io
import numpy as np
import dlib_models
from dlib_models import load_dlib_models

load_dlib_models()

from dlib_models import models


def face_detection(filepath):
    """
    Detects faces in an image, makes borders around them, and gives their descriptors

    Parameters
    --------------

    Returns
    --------------

    """
    img_array = io.imread(filepath)

    if np.size(img_array, 2) == 4:
        img_array = img_array[:, :, :4]

    face_detect = models["face detect"]

    upscale = 1

    detections = face_detect(img_array, upscale)
    detections = list(detections)

    face_borders = []
    face_descriptors = []

    for i in range(len(detections)):
        face_descriptors.append(descriptors(detections[i], img_array))

    return face_descriptors


def borders(det):
    """
    Calculates the borders for image



    """

    l, r, t, b = det.left(), det.right(), det.top(), det.bottom()
    return l, r, t, b


def descriptors(det, img_array):
    """
    Calculates and returns descriptors for all detected faces in image

    Parameters
    -----------------------
    detections: List of detected faces

    Returns
    ----------------------
    descriptors: List of descriptor numpy arrays

    """



    face_rec_model = models["face rec"]

    shape_predictor = models["shape predict"]
    shape = shape_predictor(img_array, det)
    descriptors = np.array(face_rec_model.compute_face_descriptor(img_array, shape))

    return descriptors
