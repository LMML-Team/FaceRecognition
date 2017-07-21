import numpy as np
from dlib_models import load_dlib_models

load_dlib_models()

from dlib_models import models


def face_detection(img_array):
    """
    Detects faces in an image, makes borders around them, and gives their descriptors

    Parameters
    -----------------------
    img_array: array of the image

    Returns
    -----------------------
    face_descriptors: an array of the descriptors of the detected faces

    """
    if np.size(img_array, 2) == 4:
        img_array = img_array[:, :, :4]

    face_detect = models["face detect"]

    upscale = 1

    detections = face_detect(img_array, upscale)

    face_descriptors = np.array([])

    for i in range(len(detections)):
        face_descriptors.append(descriptors(detections[i], img_array))

    return face_descriptors


def borders(det):
    """
    Calculates the borders for image
    
    Parameters
    -----------------------
    det: List of detected faces
    
    Return
    -----------------------
    l: left coordinates of the box around the face
    r: right coordinates of the box around the face
    t: top coordinates of the box around the face
    b: bottom coordinates of the box around the face
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
