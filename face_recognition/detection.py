import numpy as np
from dlib_models import load_dlib_models

load_dlib_models()

from dlib_models import models


def face_detection(img_array):
    """
    Detects faces in an image, makes borders around them, and gives their descriptors

    Parameters
    --------------
    img_array: int array
        Array representing image in which faces are to be detected

    Returns
    --------------
    face_descriptors: numpy array of descriptors for each detected face in img_array

    """
    if np.shape(img_array)[-1] == 4:
        img_array = img_array[:, :, :3]

    face_detect = models["face detect"]

    upscale = 1

    detections = list(face_detect(img_array, upscale))
    face_descriptors = np.zeros((len(detections), 128))
    face_borders = np.zeros((len(detections), 4))

    for i, det in enumerate(detections):
        face_descriptors[i] = descriptors(det, img_array)
        face_borders[i] = borders(det)

    return face_descriptors, face_borders


def borders(det):
    """
    Calculates the borders for image
    
    Parameters
    --------------
    det: int array
        Detected face
    
    Returns
    ----------------------
    l: int list
        Coordinates for left bound of border
    r: int list
        Coordinates for right bound of border
    t: int list
        Coordinates for top bound of border
    b: int list
        Coordinates for bottom bound of border
    """
    l, r, t, b = det.left(), det.right(), det.top(), det.bottom()
    return l, r, t, b


def descriptors(det, img_array):
    """
    Calculates and returns descriptors for all detected faces in image

    Parameters
    -----------------------
    det: int array
        Detected face
    img_array: int array
        Image containing the faces
    

    Returns
    ----------------------
    descriptors: list[int arrays]  
        Descriptors for det in img_array

    """
    face_rec_model = models["face rec"]

    shape_predictor = models["shape predict"]
    shape = shape_predictor(img_array, det)
    descriptors = np.array(face_rec_model.compute_face_descriptor(img_array, shape))

    return descriptors
