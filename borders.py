def borders(detections):
    import skimage.io as io
    import numpy as np
    import dlib_models
    from dlib_models import load_dlib_models

    load_dlib_models()

    from dlib_models import models


    for i in range(len(detections)):
        det = detections[i]
        l, r, t, b = det.left(), det.right(), det.top(), det.bottom()